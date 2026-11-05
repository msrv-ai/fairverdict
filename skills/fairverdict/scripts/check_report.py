#!/usr/bin/env python3
"""Check a finished FairVerdict report before it is shared.

Usage:  python3 check_report.py report.md --type short|full [--scores scores.json]

ERROR lines must be fixed before the report is shared; WARN lines deserve a look.
Exits with status 1 when there is at least one ERROR. Reads only the files it is
given, writes nothing and makes no network calls. Pass the scores.json used for
judge_score.py to check that every candidate and its score made it into the report.
"""
import argparse
import re
import sys
from pathlib import Path

FAIRVERDICT_URL = "https://msrv.dev/fairverdict"
MSRV_URL = "https://msrv.dev"
SIGNATURE = (f"*This report was made with AI. [FairVerdict]({FAIRVERDICT_URL}/) by [msrv]({MSRV_URL}) "
             "was used for objective analysis.*")
# Soft word limits as (base, per candidate) for the minimum and the maximum; tables and headings count.
WORD_LIMITS = {"short": ((0, 0), (220, 75)), "full": ((500, 170), (1000, 450))}

FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`\n]*`")
PLACEHOLDER = re.compile(r"<(?![\s=<])[^<>\n]{1,80}(?<![\s-])>")
MD_LINK = re.compile(r"\[[^\]\n]*\]\(\s*<?([^)\s>]+)>?[^)\n]*\)")
BARE_URL = re.compile(r"https?://[^\s)\]>]+")
BRACKETED_LINE = re.compile(r"^\*{0,2}\[[^\]\n]+\]\*{0,2}$")  # e.g. a leftover [Proof: ...] placeholder
CONFIG_NAME = re.compile(r"\b(?:CLAUDE|AGENTS|GEMINI|SKILL)\.md\b|\.cursorrules|\.claude/|\.codex/|"
                         r"skills/fairverdict|judge_score\.py|check_report\.py|scores\.json", re.I)
SOURCES_HEADING = re.compile(r"^#{1,6}\s*\W*\s*(?:sources?|references|bibliography|further reading|"
                             r"источники|список источников|литература|ссылки|джерела|fuentes|referencias|"
                             r"quellen|literatur|références|fontes|źródła)\b", re.I)
SCORE_OUT_OF_100 = re.compile(r"\b\d{1,3}\s*/\s*100\b")
LIST_ITEM = re.compile(r"^\s{0,3}(?:[-*+]|\d{1,2}[.)])\s+\S")
DELIMITER_CELL = re.compile(r"^\s*:?-{3,}:?\s*$")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2B55]")
ALLOWED_EMOJI = {"\U0001F947", "\u26D4"}  # the callout medal and the disqualified marker


def cells(row):
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|") and not row.endswith("\\|"):
        row = row[:-1]
    return re.split(r"(?<!\\)\|", row)


def links(line):
    return set(MD_LINK.findall(line)) | set(BARE_URL.findall(line))


def own_link(url):
    """Return "fairverdict" or "msrv" for the signature's two links, None for any other link."""
    url = url.rstrip(".,;:!?*_")
    if url.startswith(FAIRVERDICT_URL):
        return "fairverdict"
    return "msrv" if url.rstrip("/") == MSRV_URL else None


def prose_lines(lines):
    """Yield (number, line) outside fenced code, with inline code removed."""
    fenced = False
    for number, line in enumerate(lines, 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            yield number, INLINE_CODE.sub("", line)


def check_tables(prose, report, max_columns=None):
    rows = {n: line for n, line in prose}
    numbers = sorted(rows)
    i = 0
    while i < len(numbers):
        n = numbers[i]
        if not rows[n].lstrip().startswith("|"):
            i += 1
            continue
        block = [n]
        while i + 1 < len(numbers) and numbers[i + 1] == block[-1] + 1 and rows[numbers[i + 1]].lstrip().startswith("|"):
            i += 1
            block.append(numbers[i])
        i += 1
        previous = rows.get(n - 1, "").strip()
        if previous:
            report("WARN", n, "add a blank line before this table, or Reddit and many sites show it as plain text")
        header = cells(rows[block[0]])
        if max_columns and len(header) > max_columns:
            report("WARN", n, f"this table has {len(header)} columns; keep a post's tables to {max_columns} "
                              "so they read on a phone")
        if len(block) < 2 or not all(DELIMITER_CELL.match(c) for c in cells(rows[block[1]])):
            report("ERROR", n, "table needs a delimiter row such as |---|---| right after its header row")
            continue
        for row_number in block[1:]:
            count = len(cells(rows[row_number]))
            if count != len(header):
                report("ERROR", row_number, f"table row has {count} cells, its header has {len(header)}")


def check_lists(prose, report):
    rows = dict(prose)
    for n, line in rows.items():
        if not LIST_ITEM.match(line):
            continue
        previous = rows.get(n - 1, "")
        if previous.strip() and not LIST_ITEM.match(previous) and not previous.startswith((" ", "\t", "#", ">", "|")):
            report("WARN", n, "add a blank line before this list, or Reddit and many sites merge it into the paragraph")


def check_scores(path, text, kind, report):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import judge_score  # bundled with this script

    weights, cands, dq = judge_score.load(path)
    totals = judge_score.totals(cands, weights)
    lines = text.splitlines()
    headings = [line for line in lines if line.startswith("##")]  # section headings, not the H1 headline
    for name, total in totals.items():
        named = [line for line in lines if name in line]
        if not named:
            report("WARN", None, f"candidate '{name}' does not appear in the report")
            continue
        score = str(judge_score.r0(total))
        if not any(re.search(rf"(?<![\d.]){score}(?![\d])", line.replace(name, " ")) for line in named):
            report("WARN", None, f"'{name}' scored {score}/100, but no line that names it shows {score}")
        if kind == "full" and not any(name in line for line in headings):
            report("WARN", None, f"the full article has no section heading for '{name}'")
    for name in dq:
        if name not in text:
            report("WARN", None, f"disqualified candidate '{name}' is not mentioned")
    return len(totals) + len(dq)


def main():
    parser = argparse.ArgumentParser(description="Check a finished FairVerdict report.")
    parser.add_argument("report", type=Path)
    parser.add_argument("--type", choices=("short", "full"), required=True)
    parser.add_argument("--scores", type=Path, help="the scores.json used for judge_score.py")
    args = parser.parse_args()

    text = args.report.read_text(encoding="utf-8")
    lines = text.splitlines()
    problems = []

    def report(level, number, message):
        problems.append((level, number, message))

    prose = list(prose_lines(lines))
    nonblank = [(n, line) for n, line in prose if line.strip()]
    if not nonblank:
        sys.exit("error: the report is empty")

    h1 = [n for n, line in prose if re.match(r"^#\s", line)]
    if len(h1) != 1:
        report("ERROR", h1[1] if len(h1) > 1 else None, f"use exactly one H1 headline (found {len(h1)})")
    elif nonblank[0][0] != h1[0]:
        report("WARN", nonblank[0][0], "start the report with its H1 headline")

    signature_number, signature = nonblank[-1]
    if {"fairverdict", "msrv"} - {own_link(url) for url in links(signature)}:
        report("ERROR", signature_number, f"end with the signature, translated into the report's language: {SIGNATURE}")
    if not any(line.lstrip().startswith(">") and SCORE_OUT_OF_100.search(line) for _, line in prose):
        report("ERROR", None, "the verdict callout (a blockquote with the score out of 100) is missing")

    for n, line in prose:
        for match in PLACEHOLDER.finditer(line):
            inner = match.group(0)[1:-1]
            if not re.match(r"(?:https?://|mailto:)", inner):
                report("ERROR", n, f"unresolved template field or HTML tag: {match.group(0)}")
        if SOURCES_HEADING.match(line):
            report("ERROR", n, "remove the sources section: reports carry no source list")
        if BRACKETED_LINE.match(line.strip()):
            report("ERROR", n, f"remove the placeholder line {line.strip()}: reports end with the signature, "
                               "with no proof or share-link line")
        if CONFIG_NAME.search(line):
            report("ERROR", n, f"remove the configuration or internal file name: {CONFIG_NAME.search(line).group(0)}")
        urls = links(line)
        for url in sorted(urls):
            if not url.startswith("#") and not own_link(url):
                report("ERROR", n, f"remove the link {url}: reports link only to FairVerdict and msrv "
                                   "(unless the host requires inline citations)")
        if args.type == "short" and n != signature_number and any(own_link(url) for url in urls):
            report("WARN", n, "keep a post's links in the signature at the end: on Reddit, a post that opens "
                              "with a link to its maker's site, or links it twice, reads as promotion")

    check_tables(prose, report, max_columns=4 if args.type == "short" else None)
    check_lists(prose, report)
    for n, line in prose:
        extra = sorted(set(EMOJI.findall(line)) - ALLOWED_EMOJI)
        if extra:
            report("WARN", n, f"decorative emoji {' '.join(extra)}: the only emoji are the callout medal and ⛔")
        if args.type == "short" and re.match(r"^\s*(?:>\s*)?##?\s", line) and n not in h1:
            report("WARN", n, "use ### for headings in a post: # and ## render oversized on Reddit")
        if args.type == "short" and re.match(r"^\s{0,3}\+\s", line):
            report("WARN", n, "use - for bullets: Reddit doesn't render + bullets")
    if args.type == "short" and any(FENCE.match(line) for line in lines):
        report("WARN", None, "fenced code blocks break on old Reddit; quote the text or indent it by four spaces")

    candidates = check_scores(args.scores, text, args.type, report) if args.scores else 5
    words = len(re.findall(r"\w+", "\n".join(line for _, line in prose)))
    (min_base, min_per), (max_base, max_per) = WORD_LIMITS[args.type]
    low, high = min_base + min_per * candidates, max_base + max_per * candidates
    if words > high:
        report("WARN", None, f"{words} words is long for a {args.type} report on {candidates} candidates "
                             f"(aim for at most about {high}); cut repetition, not evidence")
    elif words < low:
        report("WARN", None, f"{words} words is thin for a {args.type} report on {candidates} candidates "
                             f"(about {low} or more); check that every section is there")

    errors = sum(1 for level, _, _ in problems if level == "ERROR")
    for level, number, message in sorted(problems, key=lambda p: (p[0] != "ERROR", p[1] or 0)):
        print(f"{level}{f' line {number}' if number else ''}: {message}")
    print(f"{args.type} report · {words} words · {errors} error(s), {len(problems) - errors} warning(s)"
          + (" · OK to share" if not errors else " · fix the errors, then check again"))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()

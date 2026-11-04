#!/usr/bin/env python3
"""Validate and package FairVerdict for Codex, ChatGPT and Claude.

Usage: python3 scripts/package_plugin.py [--output-dir PATH]
Only runtime components and the license are included; marketplaces stay in
the repository. The ZIP is deterministic for the same component contents.
"""

import argparse
import json
from pathlib import Path
import re
import shutil
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
FILES = ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json", "LICENSE")
COMPONENTS = ("skills", "assets")
IGNORED = {"__pycache__", ".DS_Store", "Thumbs.db", "desktop.ini", "__MACOSX"}
EXTENSIONS = {".md", ".py", ".json", ".yaml", ".yml", ".png", ".jpg", ".jpeg", ".webp", ".svg"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(root, relative):
    value = json.loads((root / relative).read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{relative}: expected a JSON object")
    return value


def validate(root):
    manifest = read_json(root, "plugin.json")
    require(manifest.get("$schema") == SCHEMA, "plugin.json: missing Agent Plugins schema")
    name, version = manifest.get("name", ""), manifest.get("version", "")
    require(isinstance(name, str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) and len(name) <= 64,
            "plugin.json: invalid plugin name")
    require(isinstance(version, str) and re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", version),
            "plugin.json: use a major.minor.patch version")
    require(not {"skills", "mcpServers", "apps", "interface"} & manifest.keys(),
            "plugin.json: portable manifest has legacy top-level fields")
    interface = manifest["extensions"]["com.openai"]["interface"]
    for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        require(isinstance(interface.get(field), str) and interface[field].strip(), f"interface.{field}: missing text")
    require(len(interface["shortDescription"]) <= 30, "shortDescription exceeds 30 characters")
    require(interface["category"] == "Productivity", "unexpected category")
    require(isinstance(interface.get("capabilities"), list), "capabilities must be an array")
    for field in ("logo", "composerIcon"):
        path = interface[field]
        require(isinstance(path, str) and path.startswith("./assets/") and ".." not in Path(path).parts,
                f"interface.{field}: expected a contained assets path")
        require((root / path).is_file() and not (root / path).is_symlink(), f"missing asset: {path}")
    for relative in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
        compatibility = read_json(root, relative)
        require((compatibility.get("name"), compatibility.get("version")) == (name, version),
                f"{relative}: name/version differ from portable manifest")
        if relative.startswith(".codex"):
            require(compatibility.get("interface") == interface, "Codex presentation differs from portable manifest")
            require(compatibility.get("skills") == "./skills/", "Codex skills path is missing")
    require((root / "skills/fairverdict/SKILL.md").is_file(), "FairVerdict skill is missing")
    require((root / "skills/fairverdict/scripts/judge_score.py").is_file(), "bundled scorer is missing")
    return manifest


def component_files(root):
    paths = [root / relative for relative in FILES]
    for component in COMPONENTS:
        directory = root / component
        require(directory.is_dir() and not directory.is_symlink(), f"missing component directory: {component}")
        for path in directory.rglob("*"):
            relative = path.relative_to(directory)
            if any(part in IGNORED for part in relative.parts) or path.suffix == ".pyc":
                continue
            require(not path.is_symlink(), f"symlinks cannot be packaged: {path.relative_to(root)}")
            if path.is_dir():
                continue
            require(not any(part.startswith(".") for part in relative.parts), f"unexpected hidden component: {relative}")
            require(path.suffix.lower() in EXTENSIONS, f"unexpected component file: {relative}")
            paths.append(path)
    for path in paths:
        require(path.is_file() and not path.is_symlink(), f"missing or linked component: {path.relative_to(root)}")
    return sorted(paths, key=lambda path: path.relative_to(root).as_posix())


def build(root, output_dir):
    manifest = validate(root)
    paths = component_files(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{manifest['name']}-{manifest['version']}.zip"
    # Stage only selected components. The archive is outside this package tree.
    with tempfile.TemporaryDirectory(prefix="fairverdict-package-") as temporary:
        stage = Path(temporary) / manifest["name"]
        for path in paths:
            target = stage / path.relative_to(root)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as package:
            for path in sorted(stage.rglob("*")):
                if path.is_file():
                    entry = zipfile.ZipInfo(path.relative_to(Path(temporary)).as_posix(), (2020, 1, 1, 0, 0, 0))
                    entry.create_system = 3
                    entry.external_attr = 0o100644 << 16
                    entry.compress_type = zipfile.ZIP_DEFLATED
                    package.writestr(entry, path.read_bytes())
    with zipfile.ZipFile(archive) as package:
        require(package.testzip() is None, "archive integrity check failed")
        expected = {f"{manifest['name']}/{path.relative_to(root).as_posix()}" for path in paths}
        require(set(package.namelist()) == expected, "archive contains unexpected files")
    return archive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    try:
        archive = build(ROOT, args.output_dir.resolve())
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(1, f"error: {error}\n")
    print(archive)


if __name__ == "__main__":
    main()

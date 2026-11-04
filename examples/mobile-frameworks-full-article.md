# React Native vs Flutter for building mobile apps fast: too close to call — what decides it (5 frameworks compared, 2026)

*November 5, 2026 · AI analysis by Claude Opus 5.5 with [FairVerdict](https://msrv.dev/fairverdict/) · 5 candidates · 6 criteria*

Picking a cross-platform framework is a bet on how quickly your team gets from idea to both app stores, so "best" here means fastest to build with, for a small team starting fresh, with runtime performance as a guardrail. We scored Flutter and the four most-adopted alternatives on six criteria fixed before any research, and checked 30 key facts against official docs and repositories. React Native, used with Expo, and Flutter finish one point apart: React Native wins the path from code to the stores, Flutter the day-to-day UI loop.

> ## Too close to call: React Native · Flutter
>
> **React Native 81 / 100 · Flutter 80 / 100** · 1 point apart · React Native takes 52% of 5,000 weight-and-score simulations, Flutter 39%
>
> The deciding priority is your release pipeline versus your UI iteration loop. Expo's cloud builds, one-command store submission and over-the-air fixes give React Native 3.0 weighted points on build and release; Flutter's stateful hot reload and built-in widget set win back 2.5 points on UI iteration speed.

**Quick picks**

- **Pick React Native if** shipping and updating matter most: it leads build and release 9 to 7.
- **Pick Flutter if** UI iteration matters most: it takes first place when that criterion counts double.
- **Pick Ionic if** your team builds for the web: it is the only candidate whose app is a web app (Angular, React or Vue) running in a WebView.

## At a glance

| Rank | Framework | Score /100 | Best for | Main trade-off |
|:---:|---|:---:|---|---|
| 1–2 | **React Native** (with Expo) | 81 | Cloud builds, store submission and over-the-air fixes in one toolchain | Expo Go on a physical iPhone needs a paid Apple Developer membership |
| 1–2 | **Flutter** | 80 | Teams that iterate on UI all day | No first-party cloud builds or over-the-air updates |
| 3 | **Ionic** (with Capacitor) | 75 | Web teams using Angular, React or Vue | UI renders in a WebView |
| 4 | **Kotlin Multiplatform** (with Compose Multiplatform) | 57* | Native code with direct platform APIs | Hot reload runs only on a desktop target |
| 5 | **.NET MAUI** | 55* | C# and .NET teams | XAML-only hot reload; no first-party cloud builds |

*\* Part of this score rests on thin evidence; see that framework's section.*

## What we compared

You want to ship one app to iOS and Android fast, so the unit is a cross-platform framework that builds both from one codebase. Tools adopted together are judged together: React Native with Expo, which the React Native docs recommend for new apps; Kotlin Multiplatform with Compose Multiplatform for shared UI; and Ionic Framework with Capacitor, its native runtime.

- **In scope:** frameworks that ship installable iOS and Android apps from one codebase, with stable support on both and a stable release in the past 12 months; current versions as of November 5, 2026.
- **Out of scope:** single-platform toolkits (SwiftUI or Jetpack Compose on their own), low-code builders, game engines, and desktop-first .NET UI frameworks such as Avalonia and Uno Platform.
- **How the candidates were chosen:** Flutter was fixed in advance. The other four were picked on three adoption signals: GitHub stars (covering all candidates), package downloads (npm for the JavaScript options, NuGet for .NET MAUI) and JetBrains' Developer Ecosystem survey (Kotlin Multiplatform, whose usage among respondents rose from 7% in 2024 to 18% in 2025). In the last 30 days the react-native package drew 61 million npm downloads and Capacitor's core 22.6 million; .NET MAUI's controls package has 29.1 million NuGet downloads in total.
- **Assumptions:** "fast" means speed of development; a small team starting fresh, with no prior commitment to a language; phone apps, not games.

## How we scored

| Criterion | Weight | What 10/10 means |
|---|:---:|---|
| Time to first app | 15% | One official command creates a project that runs on an iOS and an Android simulator or device within minutes, with templates for common app structures |
| UI iteration speed | 25% | Sub-second stateful hot reload on both platforms, a complete built-in component set, first-party inspector and debugging tools |
| Libraries & native APIs | 20% | Maintained packages for every common need (camera, maps, push, payments, auth, storage) and a simple path to native APIs |
| Learning curve | 15% | A developer new to the stack ships a first real screen in a day or two; a widely known language; abundant docs and Q&A |
| Build & release | 15% | One-command or cloud builds for both stores, managed signing and submission, over-the-air fixes where store rules allow |
| Runtime performance | 10% | Smooth 60/120 fps, fast startup and small binaries, on par with native apps in independent benchmarks |

Runtime performance is a guardrail: a framework can be quick to build with and still produce apps that feel sluggish, so it counts, with a small weight.

**Must-haves:** installable iOS and Android apps from one codebase, with stable support on both; a stable release within the past 12 months. All five pass.

The rubric was fixed before research, and every framework got the same research: four searches each with identical query patterns, plus shared searches for selection and benchmarks. Thirty key facts were checked by five independent verifiers, one per framework, against official docs and repositories. This is an analysis of published evidence (docs, release notes, benchmarks, surveys and issue reports), not hands-on testing.

## The ranking

### 1–2. React Native — 81/100, best if your release pipeline matters most

*The shortest path from code to both stores and back, paid for with a weaker UI loop than Flutter's.*

**Key facts:** React Native 0.88.1 (October 27, 2026) with Expo SDK 58 · MIT license · iOS and Android · 126.9k GitHub stars, 61 million npm downloads in the last 30 days

React Native's edge is Expo's services, now branded Expo Build, Expo Submit and Expo Update: cloud builds, store uploads and over-the-air fixes as one first-party toolchain, while Ionic's closest equivalent, Appflow, is being wound down. It trails Flutter on UI iteration, because its core component set is small and teams lean on libraries, and on runtime performance.

**Strengths**

- Release pipeline: Expo Build compiles and signs iOS and Android apps in the cloud, so iOS builds don't need your own Mac, and Expo Submit uploads to both stores with one command (Expo docs).
- The most familiar stack for a team starting fresh: JavaScript or TypeScript with React, and the React Native docs recommend starting new apps with a framework such as Expo.

**Limitations**

- Testing on a physical iPhone with Expo Go now requires an Apple Developer Program subscription and a self-built copy installed through TestFlight (Expo setup docs); on Android, Expo Go still installs from the Play Store.
- In a reproducible same-app benchmark (React Native 0.76 with the New Architecture vs Flutter), Flutter used CPU and memory more efficiently and held frame rates more steadily; React Native had a slight edge in iOS startup and app size. The benchmark predates current versions.

**Best for:** teams that want builds, submission and fixes handled by one toolchain · **Skip it if:** UI iteration speed is your top priority

### 1–2. Flutter — 80/100, best if UI iteration speed matters most

*The fastest UI loop here and a top runtime score, paid for with a release pipeline you assemble from third-party services.*

**Key facts:** Flutter 3.47 (stable since August 12, 2026; hotfix 3.47.9 on October 29) · BSD-3-Clause license · iOS and Android from one codebase · 181k GitHub stars, no published security advisories in the last 12 months

Flutter has the top score on the most heavily weighted criterion, UI iteration speed, and shares the top runtime score with Kotlin Multiplatform. It gives the lead back on build and release, where cloud builds and over-the-air updates come from third parties, and on learning curve, because Dart is new to most teams.

**Strengths**

- Stateful hot reload keeps app state while code changes apply to the running app, and DevTools adds a widget inspector, CPU profiler and memory view (Flutter docs).
- Impeller is the default renderer on iOS and on Android (API 29+ with Vulkan), and the same-app benchmark found Flutter more efficient than React Native on CPU, memory and frame stability.

**Limitations**

- Over-the-air fixes need a third-party service, Shorebird, which patches Dart code only; native changes still need a store release. CI and signing usually come from third-party tools such as Codemagic.
- The Material and Cupertino widget libraries are moving out of the core SDK into separate packages, so expect some migration work over the next releases.

**Best for:** teams that iterate on UI all day and care about smooth rendering · **Skip it if:** you want builds, submission and over-the-air fixes from one vendor

### 3. Ionic — 75/100

*The easiest start for web developers, paid for with WebView performance.*

**Key facts:** Ionic Framework 9.0.10 (October 28, 2026; version 9 announced August 19) with Capacitor 8.6.0 (October 28; Capacitor 9 in beta) · MIT license · Angular, React or Vue · 52.7k GitHub stars, 22.6 million Capacitor core downloads in the last 30 days

Ionic tops the learning curve because it is standard web development, and ties for the best time to first app. It falls behind on runtime performance, because the UI renders in a WebView, and on libraries.

**Strengths**

- Web skills carry over: Ionic Framework officially supports Angular, React and Vue, and you iterate in the browser before you test on a device.
- Fixes to the web layer can ship as live updates without a store release, through services such as Capawesome, which Ionic now recommends.

**Limitations**

- The UI runs in a WebView: Capacitor requires an Android WebView with Chrome 60 or later and uses the Android System WebView on Android 10 and up (Capacitor docs), which puts Ionic last on runtime performance.
- Ionic is winding down its commercial products, including the Appflow build and live-update service, with a final end-of-life date of December 31, 2027; Ionic Framework and Capacitor stay free and supported (Ionic blog).

**Best for:** web teams for whom runtime performance is not the priority · **Skip it if:** runtime performance matters (5 of 10, the lowest here)

### 4. Kotlin Multiplatform — 57/100

*Native code and direct platform access, paid for with the slowest UI loop and the heaviest setup.*

**Key facts:** Compose Multiplatform 1.12.2 (October 15, 2026) on Kotlin 2.4.21 · Apache-2.0 license · Kotlin Multiplatform and Compose Multiplatform both listed as Stable on iOS and Android · usage among JetBrains survey respondents up from 7% (2024) to 18% (2025)

Kotlin Multiplatform shares the top runtime score and reaches platform APIs directly, but this comparison weights development speed most, and there it trails on UI iteration speed, learning curve, and build and release.

**Strengths**

- Direct platform access: Kotlin code calls Apple system frameworks such as Foundation directly (Kotlin docs), and Google officially supports Kotlin Multiplatform for sharing business logic between Android and iOS.
- Compiled native code on both platforms. Evidence is thin on runtime performance, since no independent benchmark of Compose Multiplatform on iOS turned up; treat that score as provisional.

**Limitations**

- Compose Hot Reload runs only on a desktop (JVM) target, so UI changes on Android and iOS go through a rebuild (Kotlin docs).
- The toolchain spans Gradle, an IntelliJ-based IDE and Xcode, with no first-party cloud builds or over-the-air updates.

**Best for:** teams that need native code and direct platform APIs more than build speed · **Skip it if:** you need a first version quickly with a team new to Kotlin

### 5. .NET MAUI — 55/100

*Device APIs in the box for C# teams, paid for with a slow UI loop and a do-it-yourself release pipeline.*

**Key facts:** .NET MAUI 10 (released November 11, 2025; service release 10.0.120 on October 21, 2026; supported until May 11, 2027), with .NET MAUI 11 in release candidate · MIT license · mobile and desktop from one C# codebase · 23.3k GitHub stars, 29.1 million NuGet downloads of its controls package

.NET MAUI's best scores come from built-in device APIs (libraries), the C# learning curve and runtime performance (low confidence). It trails on UI iteration speed (low confidence), time to first app, and build and release.

**Strengths**

- Cross-platform device APIs ship in the box, including geolocation, device sensors and secure storage (Microsoft docs).

**Limitations**

- XAML Hot Reload doesn't reload C# code (Microsoft docs), so logic changes need a rebuild. Evidence is thin on UI iteration speed; treat that score as provisional.
- Visual Studio App Center, which offered cloud builds and CodePush updates, retired on March 31, 2025, and iOS builds need a Mac with Xcode, used directly or paired from Windows (Microsoft docs).

**Best for:** C# and .NET teams · **Skip it if:** you need fast UI iteration or over-the-air fixes

## Also considered

- **NativeScript** — more GitHub stars (25.7k) than .NET MAUI, but its core package drew about 96,000 npm downloads in the last 30 days (1.1 million in the past year), a sign of low current adoption.
- **Lynx** — a newer framework (15.2k stars, about 179,000 npm downloads a month for its React package); too early to judge against established options.
- **Apache Cordova** — Capacitor's predecessor, with about 271,000 npm downloads in the last 30 days against 22.6 million for Capacitor.

## Scores by criterion

| Criterion (weight) | React Native | Flutter | Ionic | Kotlin Multiplatform | .NET MAUI |
|---|---|---|---|---|---|
| Time to first app (15%) | 8 | 8 | 8 | 6 | 5 |
| UI iteration speed (25%) | 8 | 9 | 8 | 5 | 5* |
| Libraries & native APIs (20%) | 8 | 8 | 7 | 6 | 6 |
| Learning curve (15%) | 8 | 7 | 9 | 5 | 6 |
| Build & release (15%) | 9 | 7 | 7 | 5 | 5 |
| Runtime performance (10%) | 7 | 8 | 5 | 8* | 6* |
| **Total /100** | **81** | **80** | **75** | **57** | **55** |

*Scores are 0–10; \* marks low confidence.*

React Native gains 3.0 weighted points on build and release and 1.5 on learning curve; Flutter takes back 2.5 on UI iteration speed and 1.0 on runtime performance. They tie on time to first app and libraries, which leaves React Native one point ahead.

## How to choose

- **If cloud builds, store submission and over-the-air fixes matter most:** React Native — it leads build and release 9 to 7, and its lead grows to 3.5 points when that criterion counts double.
- **If UI iteration speed matters most:** Flutter — it takes first place when UI iteration counts double, and when build and release is left out.
- **If your team already builds for the web:** Ionic — the only candidate whose app is a web app running in a WebView, with the top learning-curve score; accept the lowest runtime score.
- **If you need native code and direct platform APIs more than build speed:** Kotlin Multiplatform — its code calls iOS frameworks directly, and it shares the top runtime score (low confidence).
- **If your team is a C# and .NET shop:** .NET MAUI — the only C# option here; its learning-curve score assumes a team starting fresh, so .NET experience narrows the gap.

## How solid is this verdict?

Not solid at the top. React Native takes 52% of 5,000 simulations that jitter the weights and the scores, Flutter 39% and Ionic 9%; Kotlin Multiplatform and .NET MAUI take none. Four of the 13 tested weightings put Flutter first or level: Flutter leads without learning curve (by 0.6 points), without build and release (by 2.4) and when UI iteration counts double (by 1.2), and the two tie when runtime performance counts double. React Native stays ahead under equal weights, by 1.7. Ionic's third place is steadier, five points behind Flutter; the order of Kotlin Multiplatform and .NET MAUI, two points apart with low-confidence cells, is uncertain.

**Fact-check:** 30 facts checked independently · **20 confirmed · 0 contradicted · 10 not found** · three of the not-found facts were then confirmed in official docs by this analysis itself: Compose Multiplatform's Stable status on iOS, the 7%-to-18% survey figure and Capacitor's WebView requirement.

Two scores changed. The fact-check showed that Expo Go on a physical iPhone now needs an Apple Developer membership and a TestFlight build, so React Native's time to first app dropped from 9 to 8. The bias audit then lowered React Native's libraries score from 9 to 8, because that extra point rested on npm download volume, which measures popularity rather than library coverage. Before these corrections React Native led by 4.5 points. "Not found" means a verifier couldn't confirm a fact, not that it is false.

## FAQ

### Do I need a Mac to build the iOS app?

Apple's build tools run only on macOS, so every framework here builds iOS apps on a Mac, yours or one in the cloud. Expo Build runs iOS builds in the cloud as part of React Native's own toolchain; with the others you rent macOS CI machines from a third party or use your own Mac, which .NET MAUI documents as a paired build host from Windows.

### Can I ship fixes without a store review?

Within limits: Expo Update pushes fixes straight to users, Flutter relies on the third-party Shorebird service (Dart code only), and Ionic apps can live-update their web layer through services such as Capawesome. We found no first-party option for Kotlin Multiplatform or .NET MAUI, and App Center's CodePush retired in March 2025.

### Is Ionic going away?

No. Ionic is winding down its paid products, including Appflow, with a final end-of-life date of December 31, 2027, and recommends Capawesome for native builds and live updates. Ionic Framework and Capacitor stay free and supported, and Ionic Framework 9 shipped in August 2026.

### Is Flutter still actively developed?

Yes. Flutter 3.47 reached stable on August 12, 2026, hotfix 3.47.9 followed on October 29, and the 3.50 beta appeared on November 4.

## Bottom line

Pick React Native with Expo if the path from code to the stores (cloud builds, one-command submission, over-the-air fixes) and a JavaScript or TypeScript team matter most. Pick Flutter if your time goes into iterating on UI and rendering performance matters to you. The deciding priority is release pipeline versus UI loop: leave build and release out of the score and Flutter leads by 2.4 points. Ionic is a solid third for web teams who can live with WebView performance; Kotlin Multiplatform and .NET MAUI trail on development speed.

---

[Proof: public share link not yet provided]

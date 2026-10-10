# Murim: The Ninefold Reincarnation — Master Blueprint v4.1

| Field | Value |
| --- | --- |
| Version | 4.1. Migrated target engine to Godot 4.7.2 Stable |
| Status | Binding for every coding agent and contributor |
| Engine / language | Godot 4.7.2 stable / typed GDScript |
| Platform | Android + iOS, portrait, 1080 × 1920 reference, touch-first, offline |
| Milestone covered | Milestone 1, the Vertical Slice (§3.4), built on foundations that scale (§21) |
| Working title | Configurable. Read from application/config/name; never hard-coded |

**Section map.** 0 How to use · 1 Reconciliation log · 2 Agent contract · 3 Identity and scope lock · 4 Technical foundation · 5 Anti-slop charter · 6 Data architecture · 7 Heaven’s Judgment · 8 Traits · 9 Combat rules · 10 Card catalogue · 11 Enemies and boss · 12 Map · 13 Events, rewards, merchants, rest · 14 World, factions, paths · 15 Death, Soul Fragments, hub · 16 Save system · 17 UI/UX · 18 Art, juice, audio · 19 Testing · 20 Milestones and Definition of Done · 21 Scalability roadmap · Appendix A Kickoff prompt · Appendix B Glossary

---

## 0. How to Use This Blueprint

**0.1 Purpose.** This is the single source of truth for design and implementation. An agent following it must never need to invent a number, an id, a rule, a status effect, a faction, or a line of lore. Where the blueprint specifies something, implement it exactly. Where it is silent, follow §0.6.

**0.2 Authority order** (highest first):

1. §1 Reconciliation decisions.
2. Locked values and content tables (§3.4, §7–§15).
3. Rules stated in numbered sections.
4. Existing working code in the repository (preserve unless it contradicts 1–3).
5. Agent judgment, recorded in docs/DECISIONS.md.

**0.3 Normative words.** MUST / MUST NOT are non-negotiable and are verified by a test or an inspection step. SHOULD is the default unless a recorded reason exists. MAY is optional.

**0.4 Rule IDs.** Rules carry IDs such as ARCH-01, SEC-02, CMB-14. Tests, stage reports and DECISIONS entries cite them so that every claim is traceable.

**0.5 Locked versus tunable.** *Locked* means identity and structure: counts, ids, names, rules, keyword semantics. *Tunable* means balance numbers, which live in scripts/config/game\_config.gd or in .tres content and may change without a document edit. Changing a locked value requires editing this blueprint and bumping its version first. Agents MUST NOT change locked values silently.

**0.6 Gaps.** If the blueprint is silent, choose the simplest option consistent with the five pillars (§3.2), log it in docs/DECISIONS.md (date, options considered, choice, reason), and continue. Ask the human only for the blockers listed in §2.5.

**0.7 Parameters.** Square brackets in keyword text, such as \[X\], are parameters filled from effect data. They are never literal text.

---

## 1. Reconciliation Log

The earlier drafts contradict each other in places that force an agent to guess. The decisions below are binding and override the older wording.

| # | Earlier drafts said | Binding resolution |
| --- | --- | --- |
| 1 | V1: three Karma tiers (50+, 0–49, below 0). V3: five tiers with fixed Trait Points | Five bands are the only classification (§7.4). Each band maps to one of three alignment classes used for pool weights and gating: Orthodox (20 and above), Neutral (0–19), Demonic (−1 and below). Neutral is never merged into another class |
| 2 | V1: 12–18 traits. V2: exactly 12 | Exactly 12 traits (6 positive, 6 negative). Heavenly Body is one of the six positives and is meta-locked. More traits are post-slice |
| 3 | V1: at least 24 cards. V2: exactly 24 including starters; an unlock adds five Orthodox cards | 24 library cards, five of which are Orthodox Archive cards locked until purchased. One status card (Meridian Strain) exists outside the 24 |
| 4 | V2: 5–7 scenarios. V3: five steps per run | 7 authored scenarios; each run asks 5. The 500 SF unlock adds flag-gated choices to existing scenarios, not new scenarios |
| 5 | V1: starter deck 10–12. V3: exactly 10 | Base deck is exactly 10 (5 / 4 / 1). Traits may add cards on top; the base never changes |
| 6 | V3 uses Strength without defining it; Severance says Strength/Damage; Qi Disruption says lose 1 Energy OR deal 30% less | §9.5 defines every status, per-target behavior, stacking and expiry |
| 7 | V1 lists seven enemy archetypes. V2 says exactly six (five plus boss) | 3 standard, 2 elite, 1 boss (§11). Poisoned Assassin is deferred to post-slice |
| 8 | V1: many node types. V2: 8–12 nodes. V3: bonus per floor with no floor definition | Map is five floors plus a boss floor, 10 nodes (§12). A floor is one row and counts as traversed when its node is resolved |
| 9 | V1: 48 × 48 logical px touch targets | 48 dp is about 144 reference px on a typical 1080 px-wide phone. Minimum 132, preferred 144 (§17.2) |
| 10 | V3: default texture filter Nearest | Kept for pixel art. Vector art, SVG icons and text-heavy controls override to Linear (§18.2) |
| 11 | V1: Heavy Hands penalizes Strike cards but cards are only typed as attacks | Cards carry a strike tag; only tagged cards are affected |
| 12 | V1: Weapon Master upgrades two distinct attack cards. The starter deck has one attack card type | Distinct means two different card instances, not two different card types |
| 13 | V3: Gathering Breath gives Energy next turn | Implemented as an energized bonus applied at the next player-turn start (§9.4) |
| 14 | V3: rest heals exactly 30%, rounded down. V1: Bad Blood halves rest healing | heal = floor( floor(max\_hp × 0.30) × 0.5 ) when Bad Blood is active |
| 15 | V1: Resources or JSON. V3: Resources mandatory | .tres for cards, traits, enemies, scenarios, events, unlocks, generated by tools/build\_content.gd (§6.5). JSON is used only for saves |
| 16 | V1: save-and-resume optional | Resume at map-node boundaries is required. Mid-combat state is never saved (§16.5) |
| 17 | V1: Soul Fragments for milestones. V3: fixed numbers | V3 numbers plus a once-only ledger (§15.2) |
| 18 | V3: exactly one upgrade per card | is\_upgraded is a bool. Upgraded cards are ineligible for further upgrades and are excluded from upgrade pickers |
| 19 | V1: Wandering Merchant appears when unlocked, frequency unstated | Replaces one eligible node on floors 2–4 with a configured probability. It never adds nodes (§12.4) |
| 20 | Heavenly Body unlock has no defined effect | Defined in §8.3 |

---

## 2. Agent Contract

### 2.1 Role

Senior Godot 4.7.2 / GDScript engineer, roguelike and deckbuilder systems designer, mobile UX specialist and Murim narrative designer. The deliverable is a playable game in the repository, not advice, not sample scripts, not mockups.

### 2.2 Completion standard (REAL-01)

A feature is done only when all eight hold: (1) typed data exists; (2) logic changes real game state; (3) a touch-first UI exposes it; (4) it is reachable in the normal flow; (5) feedback exists; (6) failures are handled; (7) a test or documented manual procedure proves it; (8) it is recorded in docs/PROGRESS.md with evidence. Console prints, stub buttons, descriptive-only cards, session-only currency and unreachable nodes are not features.

### 2.3 Evidence vocabulary (HONEST-01)

Every claim in a report carries exactly one tag.

- **RAN**: a command was executed and its output was seen.
- **READ**: source or scene was inspected only.
- **ASSUMED**: not verified.

The word “tested” may follow only RAN. If Godot cannot run in the agent’s environment, say so once, mark every runtime claim ASSUMED, and supply the manual procedure.

### 2.4 Phase Zero audit

Before editing anything, inspect the whole repository: structure, project.godot, Godot version, main scene, autoloads, scripts, scenes, resources, input map, assets, parse and runtime errors, partially implemented systems, existing saves. Write docs/AUDIT.md with six lists: works, partial, broken, missing, reuse, replace (each replacement names the specific defect that justifies it). Never invent files, classes, nodes or imports; confirm each exists first. If the repository is empty, create the structure in §4.2.

### 2.3b Decide, do not ask (§2.5)

Ask the human only when: (a) a file or credential needed to proceed is absent and cannot be created; (b) two locked statements contradict and §1 does not resolve it; (c) an action would destroy existing player data or history. For everything else: decide, log in DECISIONS.md, continue.

### 2.6 Session protocol (CTX-01)

Agents lose context. At the start of every session read, in order: docs/BLUEPRINT.md, docs/PROGRESS.md, docs/DECISIONS.md, docs/KNOWN\_ISSUES.md. At the end of every session update PROGRESS.md with the stage checklist (evidence tags) and the next concrete step. Chat history is never a memory store.

### 2.7 Stage report (after every stage)

Files created · Files modified · Features now working (cite rule IDs) · Design decisions · Tests run with real results (RAN) · Known issues · Next concrete step. Facts only; no celebration.

### 2.8 Output rules

- Put the exact project-relative path as a heading before every file, for example `### res://scripts/logic/combat/combat_state.gd`.
- A replacement file is always complete. Never write “rest unchanged”, never use ellipses, never substitute pseudo-code.
- When direct repository editing is available, edit the files and print only paths and short summaries.
- Every referenced resource, node and script MUST exist. Scripts MUST match their scenes.
- Soft limit of 400 lines per script; split by responsibility, not by arbitrary size.

### 2.9 Existing code policy

Preserve working behavior. Replace a system only when it blocks this blueprint, and record the defect in DECISIONS.md. A rename updates every reference in the same change.

---

## 3. Identity and Scope Lock

### 3.1 Fantasy

You die. Heaven, which is restrained, distant and occasionally sardonic, judges the life you led and decides what debt you carry. You are reborn into the Murim with half a foundation and a chance to survive. Each expedition is a life; each death leaves something behind. The long game is discovering who your choices, cultivation and past incarnations are making you into, not stacking bigger numbers.

### 3.2 Pillars

1. **Every life counts.** Runs end; consequences persist as Soul Fragments, flags and memory.
2. **The setting is the rulebook.** Qi, meridians, forms, blood prices and injuries are mechanics, not skins.
3. **Legible turns.** Every enemy action is telegraphed and every number on screen can be explained with one tap.
4. **Moral texture, not a morality meter.** Karma opens and closes opportunities. No faction is simply right.
5. **Respect the thumb.** Portrait, one-handed, interruptible, short.

### 3.3 Session shape

A full run is 20–30 minutes; dying at floor 3 is about 10. One combat is 2–4 minutes, an event 30–60 seconds, a hub visit under two minutes. Backgrounding the app at any moment is safe (§16).

### 3.4 Scope lock (Milestone 1)

Nothing beyond this table is built until the slice is playable end to end and survives an app restart.

| Area | Locked slice value |
| --- | --- |
| Region | One: Blackwater Pass |
| Heaven’s Judgment | 7 authored scenarios in 4 clusters; 5 asked per run; branching by emitted tags |
| Karma | 5 bands, centralized (§7.4) |
| Traits | 12 (6 positive, 6 negative), one meta-locked, one flag-locked |
| Starter deck | 10 cards: 5 Straight-Cut Sword, 4 Iron Shirt, 1 Gathering Breath |
| Card library | 24 cards (5 locked behind the Orthodox Archive) plus 1 status card |
| Statuses | 10 (§9.5) |
| Enemies | 3 standard, 2 elite, 1 boss |
| Combat format | One enemy per combat. Data model uses an array so groups are possible later |
| Map | 5 floors plus boss floor: 10 nodes, seeded, generated once per run |
| Events | 6 consequential events |
| Merchants | 1 regular, 1 Wandering (meta-locked) |
| Rest site | 1 type with up to 3 options |
| Meta unlocks | 4, totalling 1,000 Soul Fragments |
| Persistence | Profile save plus run save at node boundaries |
| Language | English only, localization-ready (§17.6) |

### 3.5 Explicit non-goals

Multiplayer, accounts, cloud save, analytics, ads, in-app purchases, network calls of any kind, voice acting, relics, ally companions, multi-enemy combat, inventory screens, procedural 3D, plugins. Items marked post-slice in §21 are designed for but not built.

---

## 4. Technical Foundation

### 4.1 Project settings (ARCH-01)

| Setting | Value | Reason |
| --- | --- | --- |
| application/config/name | Murim: The Ninefold Reincarnation | Single source of the title. Read with ProjectSettings; never hard-code the name in scripts or scenes |
| application/run/main\_scene | res://scenes/boot.tscn | Boot validates Content, loads Profile, then routes to the hub or the resume prompt |
| application/config/features | 4.7 and GL Compatibility | Targets Godot 4.7.2 only |
| rendering/renderer/rendering\_method (and .mobile) | gl\_compatibility | 2D game: widest device support, lowest GPU and battery cost |
| display/window/size/viewport\_width, viewport\_height | 1080, 1920 | Reference portrait resolution |
| display/window/stretch/mode, aspect | canvas\_items, expand | Resolution-independent; extra height or width is absorbed by anchors and containers |
| display/window/handheld/orientation | 1 (portrait) | Locked on both platforms |
| rendering/textures/canvas\_textures/default\_texture\_filter | 0 (Nearest) | Crisp pixel art; override rules in §18.2 |
| application/run/low\_processor\_mode | true | Turn-based; redraw only on change. All animation MUST use Tween or AnimationPlayer, never polling in \_process |
| input\_devices/pointing/emulate\_touch\_from\_mouse | true | Exercises touch paths on desktop |
| input\_devices/pointing/emulate\_mouse\_from\_touch | true (default) | Controls receive touches as mouse events. UI code MUST NOT hand-roll InputEventScreenTouch handling |
| gui/theme/custom | res://assets/theme/murim\_theme.tres | One theme for every control |
| debug/gdscript/warnings | Warn on untyped declarations, unused variables, parameters and signals, integer division, narrowing conversion, unreachable code | First-party scripts MUST open with zero warnings |
| internationalization/pseudolocalization | Off by default; on for QA with about 40% expansion | Layout test for longer strings (§19.6) |

### 4.2 Directory structure

```
res://
  project.godot
  docs/            BLUEPRINT.md AUDIT.md PROGRESS.md DECISIONS.md KNOWN_ISSUES.md ASSET_MANIFEST.md TEST_REPORT.md
  scenes/          boot.tscn  hub/  judgment/  traits/  map/  combat/  reward/  merchant/  rest/  event/  death/  ui/
  scripts/
    config/        game_config.gd
    data/          card_data.gd card_effect.gd trait_data.gd trait_effect.gd enemy_data.gd
                   intent_data.gd scenario_data.gd choice_data.gd event_data.gd unlock_data.gd
    logic/         combat/  map/  judgment/  traits/  rewards/  economy/  run/   (pure RefCounted)
    autoload/      content.gd profile.gd run_session.gd router.gd
    persistence/   save_io.gd profile_codec.gd run_codec.gd migrations.gd
    ui/            screen controllers and presenters
    debug/         debug_tools.gd   (stripped from release, SEC-07)
  content/         cards/ traits/ enemies/ scenarios/ events/ unlocks/   (generated .tres)
  assets/          art/ fonts/ theme/ audio/
  tools/           build_content.gd validate_content.gd
  tests/           run_tests.gd test_*.gd
  localization/
```

### 4.3 Autoloads: exactly four (ARCH-02)

| Autoload | Owns | Must not |
| --- | --- | --- |
| Content | Loads and validates every .tres at boot; lookups by id; reports dangling references | Mutate resources; return null without reporting |
| Profile | Permanent progression: soul\_fragments, purchased\_unlocks, unlocked\_flags, stats, settings, last\_run\_summary. Loads and saves via persistence; purchase\_unlock() | Touch RunSession or scenes |
| RunSession | The single active run state (or null). start\_run, advance\_node, apply\_combat\_result, settle\_run. Autosaves at node boundaries | Hold combat state |
| Router | All scene changes through one constant table of scene paths; fade; blocks double navigation while transitioning | Contain game rules |

Autoload scripts MUST NOT declare a class\_name equal to their singleton name. No other autoloads may be added without a DECISIONS entry that cites a shared, long-lived state need.

### 4.4 Layering and ownership (ARCH-03, ARCH-04)

Dependency direction is **UI → Session (autoloads) → Logic → Data**. Never reverse it.

- **Data** (scripts/data, content/): typed Resources. Getters and validate() only; no gameplay rules.
- **Logic** (scripts/logic): RefCounted classes, deterministic, headless-testable. MUST NOT reference Node, SceneTree, autoloads, Input, Time, DisplayServer or the global RNG. Randomness arrives as an injected RandomNumberGenerator. Operations return results and ordered event lists; they never await and never emit UI signals.
- **Session** (autoloads): wires logic to persistence and exposes state through getters and signals.
- **Presentation** (scripts/ui, scenes): renders state, calls session or logic, plays event lists with tweens. It MUST NOT contain rules, mutate state directly, or treat a Label as state.

| State | Single owner | Notes |
| --- | --- | --- |
| Permanent progression and settings | Profile | UI reads getters |
| Run: deck, HP, gold, map, flags, ledger, RNG states | RunSession.state (RunState) | Serialized by run\_codec |
| Combat: piles, HP, Energy, statuses, intent, phase | CombatState instance created by the combat scene from a RunState snapshot | Destroyed at combat end; RunSession receives one CombatResult |
| Judgment progress | JudgmentSession (RefCounted) held by the judgment scene | Result handed to RunSession |
| Trait selection | TraitSelection (RefCounted) | Applied exactly once at run start |

Combat results and rewards are idempotent: each carries a combat\_id or node\_id, and RunSession ignores a second application of the same id.

### 4.5 Determinism and RNG (DET-01)

A run has seed: int in the range 0 to 4,294,967,295, displayed as an 8-digit hex “seed code” on the death screen and in bug reports. Separate RandomNumberGenerator streams are derived so changing one system never shifts another.

| Stream | Derived from | Used for |
| --- | --- | --- |
| judgment | seed + salt | scenario selection and weighting |
| map | seed + salt | layout, node types, Wandering Merchant swap |
| combat | seed + node\_index + salt | shuffles, weighted enemy intents. Re-seeded at node entry |
| reward | seed + salt | card and gold rolls |
| event | seed + salt | event selection |
| shop | seed + salt | merchant stock |

Derivation: stream\_seed = (seed × 2654435761 + salt) mod 2^32, with salts as constants in GameConfig. Rules: global randi(), randf(), randomize() after run creation, Array.shuffle() and Array.pick\_random() are forbidden because they use the global RNG. Shuffle with a Fisher–Yates routine that takes the injected RNG. A saved RNG state is stored as a string (64-bit), because JSON numbers lose precision above 2^53.

### 4.6 Godot 4.3 guardrails (G43)

1. **No typed Dictionaries.** They arrived in 4.4. Use Dictionary with validated access, or small typed classes. Typed Arrays are fine.
2. **Nothing from 4.4+.** No @abstract, FoldableContainer, AccessKit or newer APIs. Verify every API name against the 4.3 class reference before use.
3. **FileAccess.store\_* returns void in 4.3.*\* Check FileAccess.get\_open\_error() after open and file.get\_error() after writing.
4. **JSON numbers parse as floats.** Coerce with int(), reject non-integral values where an integer is required, and store values above 2^53 as strings.
5. **Resources are shared.** load() returns a cached instance. Never mutate a .tres at runtime. Run-time card state (is\_upgraded, run-unique id) lives on a CardInstance that points at immutable CardData.
6. **Logic MUST NOT reference autoloads.** Headless script mode does not guarantee autoload singletons, and the rule keeps logic testable.
7. **No await in logic.** await is allowed only in presentation, and every awaited tween or timer needs a guard against being freed or killed.
8. **Signals:** connect once in \_ready; guard re-entry with is\_connected; disconnect or free on exit. Never connect inside \_process or button handlers.
9. **Tweens:** create with create\_tween() on the owning node, keep the reference, call kill() before replacing it.
10. **Integer math:** use floori(), roundi() and explicit casts. Never rely on the / operator between ints for percentages.
11. **Containers:** never set position or size of a container’s children by hand; use size flags and custom\_minimum\_size.
12. **Scrolling lists** use ScrollContainer with a tuned scroll\_deadzone, and children set mouse\_filter to Pass so drags scroll instead of tapping.
13. **Dynamic loads:** use preload for static paths; ResourceLoader.exists() before any computed load; never load a path built from save data.
14. **Cyclic references:** logic classes reference each other by class\_name, not preload.
15. **Freed objects:** check is\_instance\_valid() before using a Callable or node reference captured across frames.

### 4.7 Performance budgets (PERF)

Reference device: 2019 mid-range Android, 3–4 GB RAM.

| Budget | Target |
| --- | --- |
| Frame rate | 60 FPS in combat; never below 30 |
| Cold boot to title | 4 s or less |
| Scene transition | 400 ms or less including fade |
| Card play | Logic resolves within one frame; full animation 700 ms or less and skippable |
| Memory | 350 MB peak or less |
| Package size | 80 MB or less |
| Draw calls in combat | 120 or less per frame (check the Debugger monitors) |
| Textures | 2048 × 2048 maximum; icons packed in atlases |
| \_process usage | None in static UI; none in logic |
| Particles | 64 live at once or fewer; none looping while idle |
| Allocations | No per-frame allocation in any code that runs every frame |
| Content load | Slice content ready in 150 ms or less; otherwise lazy-load per screen |

Performance claims in reports MUST carry a RAN tag with the measured number, or be omitted.

### 4.8 Security and integrity (SEC)

- **SEC-01.** No network use at all: no HTTPRequest, WebSocket or multiplayer nodes. The Android export preset leaves INTERNET unchecked (verify in the export dialog).
- **SEC-02.** Never load() or ResourceLoader.load() anything under user://. A .tres or .res can embed scripts, which would make a save file an execution vector. User data is JSON only.
- **SEC-03.** Forbidden calls: str\_to\_var, bytes\_to\_var\_with\_objects, var\_to\_bytes\_with\_objects, Expression, OS.execute, OS.create\_process, ClassDB.instantiate or load() with a string that comes from data.
- **SEC-04.** Every deserialized value passes validation against allowlists. Ids must exist in Content; numbers are clamped to configured ranges; arrays are capped (deck 100, flags 256); id strings are at most 64 characters; files over 1 MB are rejected before parsing.
- **SEC-05.** No secrets in the repository. .gitignore covers .godot/, keystores, provisioning profiles and export credentials.
- **SEC-06.** Local saves are tamperable. Do not claim anti-cheat or integrity protection anywhere in code, UI or documentation.
- **SEC-07.** Debug tools (grant currency, skip floor, force seed) live only in scripts/debug/debug\_tools.gd, run only when OS.is\_debug\_build() is true, and are absent from release behavior.
- **SEC-08.** No personal data is collected, stored or transmitted. Diagnostics use push\_error and push\_warning plus a visible recovery state; print() appears only in tests.
- **SEC-09.** No third-party plugins. Every font or audio file ships with its license text in assets/ and a line in docs/ASSET\_MANIFEST.md.

### 4.9 Commands the agent uses (and reports as RAN only if executed)

- Import resources: `godot --headless --path . --import`
- Build content: `godot --headless --path . --script res://tools/build_content.gd`
- Validate content: `godot --headless --path . --script res://tools/validate_content.gd`
- Run tests: `godot --headless --path . --script res://tests/run_tests.gd` (non-zero exit code on any failure)
- Syntax check one script: `godot --headless --path . --check-only --script <path>`
- Play: open in the 4.7.2 editor and run the main scene, or `godot --path .`

If the Godot binary is unavailable, record that in docs/TEST\_REPORT.md and follow §2.3.

---

## 5. Anti-Slop Charter

**5.1 Definition.** Slop is output that looks finished but is generic, unverified, redundant or fake. It is the default failure mode of generated work. This charter names the specific patterns that are forbidden in this project and how each is detected. It is binding at every stage.

**5.2 Enforcement (SLOP-01).** (a) tests/test\_slop\_scan.gd scans scripts and content for every pattern marked *auto* below and fails the test run on any hit. (b) Every stage ends with the Slop Audit in §5.8, recorded in docs/PROGRESS.md. (c) A stage cannot be reported complete while a hit is open.

### 5.3 Visual slop

| Banned (detection) | Required instead |
| --- | --- |
| Default gray Godot buttons or panels on any shipped screen (manual) | The project Theme (§18) applied everywhere. No control relies on engine defaults |
| Purple-to-blue gradients, neon glow, glassmorphism, shadows used as fake depth (manual) | Flat ink and paper surfaces. Depth from overlap, scale and value contrast |
| Gold borders on everything; decorative empty panels (manual) | Frames only where they carry meaning: card type, rarity, locked state. Empty space stays empty |
| One identical rounded rectangle for every card (manual) | Five distinct card frames by card type (§18.4) |
| Always-on particles, lens flare, constant pulsing (manual, plus the particle budget in §4.7) | Feedback only in response to an event, 300 ms or less, disabled under Reduce Motion |
| Emoji or stock fantasy icons: flaming swords, crystal orbs, generic shields (manual) | Original SVG or drawn icons from the project icon set, each paired with a text label |
| Fake brush fonts for body text; more than three type sizes on one screen (manual) | One serif for titles, one highly readable face for body (§18.3) |
| Text over busy art without a scrim (manual) | Text sits on paper or on a solid scrim at 4.5:1 contrast or better |
| Color as the only signal (manual) | Every status, faction and card type has a glyph and a word as well as a color |
| Placeholder art presented as final (manual, checked against ASSET\_MANIFEST) | Files named placeholder\_\* and marked in ASSET\_MANIFEST until replaced |

### 5.4 Writing slop

**Banned words** (auto, case-insensitive, in content and UI strings): ethereal, tapestry, testament, mystical, shrouded, unleash, symphony, eldritch, cosmic, immense power, ancient power, destiny awaits, forbidden knowledge, unimaginable, legendary, epic.

**Banned constructions** (manual unless marked): the “not X, but Y” pivot; stacked triples of adjectives; opening a text on weather or ambience; announcing a mood instead of showing a detail (“an ominous silence falls”); a rhetorical question ending a paragraph; metaphors built on whispers of, echoes of, the weight of; exclamation marks in narrative text (zero, auto) and more than one per 100 UI strings; more than one em dash per text block; the words suddenly and somehow; encouragement copy such as Great job or Well done.

**Required:**

- Every scenario, event and Heaven line contains at least two concrete particulars: a sum, a place, an object, a rank, a name.
- Characters reveal motive through an action or a demand, not an adjective.
- UI sentences are 22 words or fewer. Heaven’s lines are 20 words or fewer.
- Flavor text is one line of 12 words or fewer.
- Names are original, Korean-romanized or invented, and never borrowed from an existing franchise.

### 5.5 Design slop

- **Number-swap cards.** Every card spec states its job in one sentence: the decision it creates. Cards with the same job are merged or differentiated. (manual)
- **Rarity inflation.** Only Common, Uncommon and Rare exist in the slice. No Legendary, Epic or Mythic. (auto)
- **Fake choices.** An option that strictly dominates, options that all end the same way, or an option whose tone marks it as the trap. Every choice has a real cost and a real benefit. (manual)
- **Moral binaries.** No Good or Evil labels in UI. Every faction shows both virtue and vice (§14). (manual)
- **Empty branches.** No locked button without an unlock path that is implemented in the slice. (test)
- **Hidden math.** Every modifier that changes a displayed number appears in the tooltip breakdown. (manual)
- **Degenerate loops.** No unbounded Energy, draw or Block (guards in §9.8). (test)

### 5.6 Code slop

Auto-detected by tests/test\_slop\_scan.gd unless marked manual:

- `print(` outside tests; TODO, FIXME, HACK.
- randi(, randf(, randomize(, shuffle(, pick\_random( (global RNG, §4.5); every call forbidden by SEC-03.
- get\_node paths containing .. ; res://scenes paths outside router.gd.
- Trait, card or enemy behavior chosen by comparing an id string inside scripts/logic.
- await inside scripts/logic; \_process inside scripts/ui unless allowlisted; any script over 400 lines; functions whose whole body is pass.
- Manual review: commented-out code; magic gameplay numbers in logic; the same rule implemented in two places; push\_warning followed by returning a success value; container children positioned by hand; abstractions with fewer than two real users.

Required: typed signatures, handled Error codes, is\_instance\_valid on captured nodes, and a unit test for every logic rule.

### 5.7 Process slop

- Claiming completion because a file exists, or marking a phase complete because scripts exist.
- Tests with no assertions, tests that assert constants, deleting or loosening a test to turn it green.
- Mock data inside shipped flows, references to assets that do not exist, invented class or method names.
- Rewriting working files wholesale without a DECISIONS entry; unrelated reformatting inside a feature change.
- Reports without evidence tags (§2.3), or reports that praise instead of state facts.

### 5.8 Slop Audit (end of every stage)

Answer yes or no with a file path as evidence, in PROGRESS.md:

1. Does the scan test pass?
2. Does every screen use the project Theme?
3. Does every new card, trait and event have a distinct job?
4. Is every new string free of banned words and constructions?
5. Is every new number in GameConfig or content?
6. Does every locked element have a working unlock path?
7. Is every claim in the report evidence-tagged?
8. Are all referenced assets present?
9. Are touch targets and text sizes within §17.2?
10. Did any file change that the stage did not need?

---

## 6. Data Architecture and Content Pipeline

**6.1 Principles (DATA-01).** Data defines, logic executes, UI presents. Content Resources are immutable at runtime. Ids are snake\_case, at most 48 characters, unique per type and never reused. Renaming a shipped id requires an entry in persistence/migrations.gd (ID\_ALIASES) so old saves keep working.

### 6.2 Resource classes (one typed file each in scripts/data/)

| Class | Fields |
| --- | --- |
| CardData | id; display\_name; style (SWORD, FIST, BODY, MOVEMENT, INTERNAL, FORBIDDEN); faction (STARTER, NEUTRAL, ORTHODOX, DEMONIC); card\_type (ATTACK, TECHNIQUE, STANCE, STATUS); rarity (STARTER, COMMON, UNCOMMON, RARE); energy\_cost; blood\_price (0 = none; a non-zero value replaces the Energy cost); targeting (SELF, ENEMY); tags (strike, sword, fist…); retain; exhaust; unplayable; effects: Array\[CardEffect\]; upgrade\_effects: Array\[CardEffect\] (empty = reuse base); upgrade\_energy\_cost and upgrade\_blood\_price (−2 = unchanged); unlock\_flag (empty = always available); job (one-sentence design purpose, never shown to players); flavor; icon\_id |
| CardEffect | kind (EffectKind); amount; amount\_b; hits (default 1); status\_id; who (ACTOR, OPPONENT); condition (NONE, PREV\_CARD\_ATTACK, ACTOR\_HAS\_BLOCK, OPPONENT\_HAS\_STATUS); condition\_arg |
| EffectKind (13) | DAMAGE, DAMAGE\_FROM\_BLOCK, DRAIN, BLOCK, DOUBLE\_BLOCK, HEAL, ENERGY, ENERGY\_NEXT\_TURN, DRAW, DISCARD\_HAND\_DRAW\_PLUS, APPLY\_STATUS, LOSE\_HP, ADD\_STATUS\_CARD (enemy intents only). Exhaust is a card flag, not an effect |
| TraitData | id; display\_name; description (generated); category (CONSTITUTION, INTERNAL\_ENERGY, MARTIAL\_APTITUDE, FORTUNE, FORBIDDEN\_ARTS, PAST\_LIVES); points (the balance change for the player: negative costs points, positive grants them); requires\_profile\_flags; requires\_judgment\_flags; requires\_alignment (empty = any); excludes (trait ids); effects: Array\[TraitEffect\]; icon\_id |
| TraitEffect | kind (13 kinds, §8.2); amount; arg |
| EnemyData | id; display\_name; tier (STANDARD, ELITE, BOSS); faction; max\_hp; portrait\_id; phases: Array\[EnemyPhase\]; gold\_min; gold\_max |
| EnemyPhase | enter\_at\_hp\_pct (100 for the first phase); entry\_effects: Array\[CardEffect\]; intents: Array\[IntentData\]; sequence: Array\[StringName\] (empty = weighted selection; otherwise intent ids played in order, looping) |
| IntentData | id; kind (ATTACK, DEFEND, BUFF, DEBUFF, SPECIAL); display\_name; tell (plain-language preview); damage; hits; block; effects: Array\[CardEffect\]; weight; max\_consecutive (default 2); requires\_stance and sets\_stance (optional) |
| ScenarioData | id; cluster; prompt; speaker (optional); can\_be\_root; tag\_affinity (tag to float); requires\_flag (optional); choices: Array\[ChoiceData\] |
| ChoiceData | id; label; follow\_up (optional); karma\_delta (−12 to +12); tags (at most 2); grants\_flags; requires\_flag (profile flag; empty = always shown) |
| EventData | id; title; body; requires\_flag (optional); choices: Array\[EventChoice\]. EventChoice: label; requirements (gold, injury, flag); outcomes: Array\[EventOutcome\]. EventOutcome kinds: GAIN\_GOLD, LOSE\_GOLD, HEAL, LOSE\_HP, MAX\_HP\_ADD, ADD\_CARD, REMOVE\_CARD\_PICK, UPGRADE\_CARD\_PICK, ADD\_STATUS\_CARD\_TO\_DECK, SET\_RUN\_FLAG, START\_COMBAT |
| UnlockData | id; display\_name; cost; description; grants\_flags; requires\_unlocks |

**6.3 Generated text (DATA-02).** Card, trait, intent and status descriptions are generated from data by a text builder. No gameplay number is typed into a description or UI string. Keyword reminder text is defined once (§9.7). Upgraded values render highlighted. Tests assert that the generated text contains each effect’s numeric value, which makes text and rules impossible to desynchronize.

**6.4 Configuration (CFG-01).** scripts/config/game\_config.gd holds every tunable value in prefixed groups: PLAYER\_, COMBAT\_, KARMA\_, TRAIT\_, MAP\_, ECON\_, SOUL\_, UI\_, SAVE\_, RNG\_SALT\_, plus KNOWN\_FLAGS (the registry of every legal flag string). A gameplay number written as a literal inside scripts/logic is a defect. Permitted literals: 0, 1, −1 and array indices.

**6.5 Content pipeline (DATA-03).** Hand-writing .tres files is brittle (sub-resources, ext\_resource ids, script references). Therefore:

1. Content definitions are written as GDScript in tools/content\_defs/ and tools/build\_content.gd instantiates the typed Resources and writes them with ResourceSaver into content/.
2. The generated .tres files are committed. They are valid, inspector-editable and the runtime source.
3. When Milestone 2 starts, tools/content\_defs/ is deleted (history keeps it) so that exactly one source of truth remains: the .tres files. Record the deletion in DECISIONS.md.
4. Never hand-invent uid:// values or load\_steps.

**6.6 Validation (CONTENT-01).** ContentValidator runs at boot and in tests. In debug builds an error shows a full-screen report; in release builds the invalid entry is skipped, logged, and replaced by a safe fallback. It checks: unique ids per type; every reference resolves (flags exist in KNOWN\_FLAGS, card ids in trait effects, intent ids in sequences, unlock grants); counts match the scope lock (24 cards, 12 traits, 6 enemies, 7 scenarios, 6 events, 4 unlocks); costs and amounts are within configured ranges; every non-status card has at least one effect; every enemy phase has at least one intent; generated descriptions are 160 characters or fewer; every locked content item names an unlock source that exists.

---

## 7. Heaven’s Judgment

### 7.1 Voice bible (VOICE-01)

Heaven is restrained, distant, occasionally sardonic and hard to read. It has judged countless lives without understanding suffering, so it counts debts, not feelings.

- Second person, present tense, 20 words or fewer per line. It speaks in concrete debts: coins, names, blades, rice.
- It never explains game systems, never praises or consoles, never says good, evil, or Karma as a score.
- Each slot (opening, between questions, verdict per band, memory line) has at least three variants. A line is used at most once per judgment.
- Anchor lines set the register only. Final lines MUST be written fresh in this register and never copied: Opening: “Eleven coins were still in your sleeve. Start there.” Between questions: “You answered quickly. Quick answers are cheap.” Righteous: “The ledger leans your way. It has been wrong before.” Neutral: “Balanced. I distrust balance.” Tainted: “The debt is real. So is your reason. I record both.” Asura: “You paid in advance. How rare.” Memory (flag unlocked\_past\_betrayal): “I see you remember the blade in your back.”

### 7.2 Flow and states (JUDGE-01)

Screen order: death vignette (three visual beats, 8 seconds or less, skippable after the first viewing) → Heaven’s opening line → five question steps → verdict → trait selection.

JudgmentSession states: INTRO → ASKING → AWAITING\_CONFIRM → ASKING (next step) → … → VERDICT → DONE. Any transition outside this graph is rejected and logged.

**Question screen.** Scenario text sits in a ScrollContainer with an optional context line above it. Three to five choice buttons, each at least 144 px tall. Tapping a choice selects it and reveals a Confirm button; only Confirm commits. After commit, input is disabled until the next scenario is on screen, so a double tap cannot submit twice. There is no undo after Confirm. A menu action Restart Judgment (with confirmation) exists until the verdict. Progress is five ink dots and the text “3 of 5”.

**Verdict screen.** Heaven’s line first, then: the Karma score; the band name; two generated summary lines from the player’s top two tags; the Trait Points with the reason (for example: Karma 34 is in the Positive band, so 8 points); the perks gained; which card pools are favored; and every locked trait with its exact unmet requirement.

**Recovery (JUDGE-02).** If fewer than five valid scenarios are available at runtime, show a “Heaven is silent” screen, log the cause, and offer Retry or Begin with a neutral judgment (Karma 0, no flags). The player is never left on an empty screen.

### 7.3 Selection and branching (JUDGE-03)

Clusters: MORAL\_DILEMMA (2 scenarios), SELF\_PRESERVATION (2), SECT\_LOYALTY (2), FORBIDDEN\_TEMPTATION (1). Tags: altruistic, dutiful, pragmatic, ruthless, defiant, cynical. A choice emits at most two tags and a Karma delta from −12 to +12.

1. Step 1 draws uniformly from scenarios with can\_be\_root = true (all except the forbidden-temptation scenario).
2. Steps 2–5 draw by weight: weight = 1 + sum over tags of (affinity\[tag\] × tag\_count\[tag\] ÷ steps\_done). A scenario appears at most once per run, never shares a cluster with the previous step, and FORBIDDEN\_TEMPTATION cannot be step 1.
3. Scenarios and choices gated by a flag the player lacks are removed before weighting.
4. All draws use the judgment RNG stream, so a seed reproduces the exact judgment.
5. Karma range is therefore −60 to +60. A test MUST prove that all five bands are reachable and that the extremes are reachable.

### 7.4 Karma bands, Trait Points and perks (single table: GameConfig.KARMA\_BANDS)

| Band | Karma | Alignment class | Trait Points | Perk id |
| --- | --- | --- | --- | --- |
| Righteous | 50 and above | Orthodox | 10 | orthodox\_standing |
| Positive | 20 to 49 | Orthodox | 8 | orthodox\_leaning |
| Neutral | 0 to 19 | Neutral | 6 | open\_road |
| Tainted | −1 to −20 | Demonic | 4 | marrow\_initiate |
| Asura | −21 and below | Demonic | 2 | marrow\_adept |

Perks are checked inside gameplay systems, never only hidden in UI:

- **orthodox\_standing:** Orthodox pool weight 2.5; grants run flag iron\_principle\_favor.
- **orthodox\_leaning:** Orthodox pool weight 2.0.
- **open\_road:** the first card reward offers four cards, at least two from the Neutral pool; Neutral pool weight 1.5.
- **marrow\_initiate:** Demonic cards enter the pool at weight 2.0; the first card reward is guaranteed to include one Demonic card.
- **marrow\_adept:** everything in marrow\_initiate at weight 2.5, plus Blood Price HP costs reduced by 1 (minimum 1) and Drain effects healing 25% more (rounded down).

**Card pool weights by band.** Locked means excluded until the run flag marrow\_pact is set by event E4 (§13.2).

| Band | Orthodox pool | Neutral pool | Demonic pool |
| --- | --- | --- | --- |
| Righteous | 2.5 | 1.0 | Locked, then 0.5 |
| Positive | 2.0 | 1.0 | Locked, then 0.5 |
| Neutral | 1.0 | 1.5 | Locked, then 1.0 |
| Tainted | 0.5 | 1.0 | 2.0 |
| Asura | 0.5 | 1.0 | 2.5 |

The five Orthodox Archive cards additionally require the profile flag orthodox\_archive\_1 in every band. No band ever has weight zero for a pool it can reach, so Karma shifts opportunities without forbidding a playstyle.

### 7.5 The seven scenarios (content lock)

Write the final prose fresh, following §5.4. Situations below fix the facts; choices fix the numbers. Gated choices appear only when the profile flag unlocked\_past\_betrayal is owned.

| Scenario (cluster) | Situation | Choices (Karma; tags) |
| --- | --- | --- |
| S1 medicine\_case (Moral Dilemma) | A wounded escort lies beside a sealed medicine case on the Qinghe Ford road. The caravan guards say it belongs to the ford village. A dying stranger begs you to carry it to his daughter, two valleys east | Return it to the guards (+6; dutiful). Carry it east and answer for the theft (+9; altruistic, defiant). Split the doses and trace the supplier for more (+12; altruistic, pragmatic). Sell it to the physician bidding forty silver (−10; ruthless, pragmatic). Gated: ask who sealed it, and why, before touching it (0; cynical) |
| S2 frostbitten\_collector (Self-Preservation) | A frostbitten Iron Principle tax collector asks for your only cloak. Shelter is a night’s walk away. In the last village a farmer showed you the bruise this man left over a late payment | Give him the cloak and walk on (+11; altruistic). Leave him flint and tinder and keep the cloak (+3; pragmatic). Take his ledger of debts and seal, and leave him where he sits (−4; defiant, ruthless). Walk past without a word (−9; ruthless) |
| S3 deserters\_name (Sect Loyalty) | Your instructor orders you to strike a deserter’s name from the roll and watch his crippling at dawn. The deserter is Han Seo-jun, who taught you the basic form | Attend and say nothing (−6; dutiful). Petition the elders for a hearing before dawn (+4; dutiful). Warn him to flee tonight and lie about it (+9; altruistic, defiant). Take his place at the post (+12; altruistic, defiant). Gated: ask what he saw that made him run (0; cynical) |
| S4 burning\_the\_manual (Sect Loyalty) | An elder of the Iron Principle orders you to burn a manual. Rumor says its breathing method stopped a fever among Crimson Marrow orphans at Dongmun | Burn it as ordered (+2; dutiful). Copy it first, then burn the original (+6; pragmatic). Carry it to the Marrow healers (+11; altruistic, defiant; grants shielded\_marrow). Keep it and say nothing (−10; ruthless, pragmatic) |
| S5 blade\_that\_keeps\_ledgers (Forbidden Temptation) | At a collapsed shrine a blade offers speed beyond your years. The price is a span of your next life, collected in the next incarnation | Accept the full price (−12; ruthless). Bargain for half the speed at half the price (−4; pragmatic). Leave it untouched (+6; dutiful). Shatter it and accept whatever binds you (+8; defiant) |
| S6 orphanage\_ledger (Moral Dilemma) | An Iron Principle patrol offers one thousand silver for the location of a Crimson Marrow orphanage sheltering plague patients. You know the road to it | Give them the location (−10; ruthless, dutiful; grants informer). Warn the orphanage and refuse any reward (+12; altruistic, defiant; grants shielded\_marrow). Take the silver, then warn the orphanage (+2; pragmatic, defiant). Withhold the location until the orphanage’s healer treats your wound (−2; pragmatic). Gated: ask the patrol who posted the bounty (0; cynical) |
| S7 debt\_of\_strangers (Self-Preservation) | Heaven asks directly: a stranger will die unless someone takes on a debt, and the debt falls on your family if you do. Do you? | Yes, my family would do the same (+9; altruistic). No (−8; ruthless). Ask how large the debt is first (+1; pragmatic). Take the debt on myself instead (+12; altruistic, defiant; grants martyr) |

Tag affinities (starting values, tunable): S3 and S4 favor dutiful and defiant; S5 favors ruthless and pragmatic; S6 favors altruistic and ruthless; S2 and S7 favor pragmatic and altruistic; S1 favors none.

### 7.6 Flags and consequences (no empty branches)

| Flag | Granted by | Gameplay effect |
| --- | --- | --- |
| shielded\_marrow | S4 Carry it to the Marrow healers; S6 Warn the orphanage | Event E4 offers the clinic’s care with no injury |
| informer | S6 Give them the location | The Crimson Marrow Cultivator elite starts combat with Strength 2 |
| martyr | S7 Take the debt on myself | +50 starting Gold and −5 Max HP |
| iron\_principle\_favor | Righteous band | Event E3 offers Request Instruction |
| cynic\_route | Verdict, when profile flag unlocked\_past\_betrayal is owned and the cynical tag count is 2 or more | Makes the trait Remembered Blade selectable; Heaven speaks its memory line |

### 7.7 Result record

JudgmentResult: karma (int); band\_id; alignment\_class; tag\_counts; flags (Array\[String\]); choice\_log (scenario\_id and choice\_id per step); trait\_points; perk\_ids; summary\_lines. It is stored in RunState.judgment and is never recomputed from UI state. Summary lines come from one template per tag (six templates, 18 words or fewer, written in the §7.1 register).

---

## 8. Traits

### 8.1 Economy rules (TRAIT-01)

Balance is the Trait Point allowance from §7.4. In the sticky header show four numbers at all times: **Allowance**, **Gained** (from negative traits), **Spent** (on positive traits), **Remaining** = Allowance + Gained − Spent.

1. Toggling is always allowed, except locked traits, excluded pairs and the caps below. If Remaining is below zero, it is shown in the accent color with the sentence “Needs N more points” and Confirm is disabled. Toggling a trait back restores the balance exactly.
2. Caps: at most 6 selected traits (TRAIT\_MAX\_SELECTED) and at most 8 points gained from negative traits (TRAIT\_MAX\_NEGATIVE\_POINTS). A trait that would break a cap is disabled with the reason shown.
3. Exclusions are symmetric. A trait excluded by a selected one is disabled and names its partner.
4. Locked traits show a lock glyph and generated requirement text that names where to unlock them (§8.3). They cannot be selected.
5. Every row shows name, category glyph, points, and one generated line stating the exact penalty or benefit, so the cost is visible before selecting. The info button opens full numbers.
6. Categories appear as sections: Constitution, Internal Energy, Martial Aptitude, Fortune, Forbidden Arts, Past Lives.
7. Confirm writes trait ids to RunState.traits once and disables itself. An empty selection is legal.
8. Selection logic lives in TraitSelection (RefCounted) and is tested without UI.

### 8.2 The twelve traits (content lock)

Points use the player’s view: negative spends, positive grants.

| ID and name | Category | Points | Effect data | Rules |
| --- | --- | --- | --- | --- |
| shattered\_core, Shattered Core | Constitution | +4 | MAX\_HP\_PCT −25 | Final max HP = max(30, floor(modified × 75 ÷ 100)); the baseline result is 60. Excludes heavenly\_body |
| heavy\_hands, Heavy Hands | Martial Aptitude | +3 | STRIKE\_COST\_FIRST\_TURN +1 | Cards tagged strike cost +1 Energy during player turn 1 of each combat only. Excludes wounded\_dantian |
| bad\_blood, Bad Blood | Constitution | +2 | REST\_HEAL\_PCT −50 | Rest-site recovery only |
| wounded\_dantian, Wounded Dantian | Internal Energy | +3 | FIRST\_TURN\_ENERGY\_ADD −1 | Turn 1 of each combat starts with 2 Energy. Excludes meridian\_prodigy and heavy\_hands |
| hollow\_purse, Hollow Purse | Fortune | +2 | START\_GOLD\_ADD −60 | Start with 40 Gold |
| remembered\_blade, Remembered Blade | Past Lives | +3 | COMBAT\_START\_STATUS vulnerable 1 | Locked: needs profile flag unlocked\_past\_betrayal and judgment flag cynic\_route |
| meridian\_prodigy, Meridian Prodigy | Internal Energy | −5 | MAX\_ENERGY\_ADD +1 | Max Energy 4. Excludes wounded\_dantian |
| weapon\_master, Weapon Master | Martial Aptitude | −3 | UPGRADE\_START\_ATTACKS 2 | Upgrades the first two eligible attack card instances in deck order; with fewer than two eligible, upgrade what exists and raise no error |
| thick\_skin, Thick Skin | Constitution | −2 | START\_BLOCK 5 | 5 Block at combat initialization, not every turn |
| clear\_meridians, Clear Meridians | Internal Energy | −2 | FIRST\_TURN\_DRAW\_ADD +1 | Draw 6 on turn 1 of each combat |
| blood\_debt, Blood Debt | Forbidden Arts | −3 | ADD\_START\_CARD blood\_burning\_palm; COMBAT\_START\_HP\_LOSS 3 | Requires Demonic alignment class. The HP loss cannot reduce HP below 1 |
| heavenly\_body, Heavenly Body | Constitution | −4 | MAX\_HP\_ADD +10; COMBAT\_START\_STATUS unshakable\_stance 4 | Locked: profile flag trait\_heavenly\_body (Hub, 300 Soul Fragments). Excludes shattered\_core |

TraitEffectKind (13): MAX\_HP\_ADD, MAX\_HP\_PCT, MAX\_ENERGY\_ADD, START\_GOLD\_ADD, START\_BLOCK, STRIKE\_COST\_FIRST\_TURN, REST\_HEAL\_PCT, UPGRADE\_START\_ATTACKS, ADD\_START\_CARD, FIRST\_TURN\_ENERGY\_ADD, FIRST\_TURN\_DRAW\_ADD, COMBAT\_START\_HP\_LOSS, COMBAT\_START\_STATUS. One function resolves every kind in one place (trait\_effects.gd). Behavior is never chosen by comparing a trait id.

### 8.3 Locked traits and their unlock paths

- **Heavenly Body:** purchase the Hub unlock heavenly\_body (300 SF); it grants flag trait\_heavenly\_body. Before purchase the row reads: Unlock in the Hub, Heavenly Body, 300 Soul Fragments.
- **Remembered Blade:** needs the Hub unlock heavens\_memory (500 SF, flag unlocked\_past\_betrayal) and the cynic\_route judgment flag (§7.6). Both unmet requirements are listed separately.
- **Blood Debt:** needs the Tainted or Asura band. The row reads: Requires Demonic alignment (Karma below 0).

### 8.4 Application order (TRAIT-APPLY)

Traits apply exactly once at run creation, in this order:

1. Base values: Max HP 80, Gold 100, Energy 3, draw 5.
2. Additive modifiers: MAX\_HP\_ADD, START\_GOLD\_ADD, MAX\_ENERGY\_ADD, and judgment-flag effects (martyr).
3. Percent modifiers: MAX\_HP\_PCT, then clamp max HP to at least MIN\_MAX\_HP (30).
4. Starting deck: the 10 base cards in the fixed order Straight-Cut Sword ×5, Iron Shirt ×4, Gathering Breath; then ADD\_START\_CARD; then UPGRADE\_START\_ATTACKS.
5. Current HP is set to max HP. RunState.traits\_applied becomes true; a second call is a no-op.

Combat-level effects (START\_BLOCK, STRIKE\_COST\_FIRST\_TURN, FIRST\_TURN\_*, COMBAT\_START\_*) are never stored. CombatInit derives them from the trait list at each combat start, with traits sorted by id for a stable order, and is guarded by combat\_id against double initialization.

Rest-site healing: heal = floor( floor(max\_hp × 30 ÷ 100) × (100 + REST\_HEAL\_PCT) ÷ 100 ), then limited to max\_hp − current\_hp.

---

## 9. Combat Rules

Combat is the most important system. It is a deterministic state machine in scripts/logic/combat/ with no Node dependencies. The presenter animates what the engine already resolved.

### 9.1 Authoritative state (CMB-01)

CombatState (RefCounted) is the only owner of these fields; the UI renders them and never copies them.

- **Identity:** combat\_id, phase, turn\_number, injected combat RNG, immutable CombatModifiers snapshot (traits and perks).
- **Player:** hp, max\_hp, block, energy, max\_energy, next\_turn\_energy, statuses.
- **Enemies:** Array\[EnemyState\] (exactly one in the slice): hp, max\_hp, block, statuses, phase\_index, pending\_phase, current intent, intent history, stance, sequence\_index.
- **Piles:** draw\_pile, hand, discard\_pile, exhaust\_pile, each an Array\[CardInstance\]. CardInstance = instance\_id (int), data (CardData), is\_upgraded (bool).
- **Turn trackers:** cards\_played\_this\_turn, last\_card\_type\_this\_turn (for Form).
- **Outcome:** ONGOING, VICTORY or DEFEAT, latched; reward\_eligible is true only after VICTORY and only until claimed.
- **Target:** the current target index (always 0 in the slice).
- **Event log:** the ordered CombatEvent list drained by the presenter.

### 9.2 Phases and actions (CMB-02)

Phases: SETUP → PLAYER\_TURN → ENEMY\_TURN → PLAYER\_TURN … with VICTORY and DEFEAT as terminal latches (no transition out). The engine exposes exactly two player actions: play\_card(instance\_id, target\_index) and end\_turn(). Each returns an ActionResult (ok, reason\_code, events) and is valid only in PLAYER\_TURN. The enemy phase runs synchronously inside end\_turn(), so no asynchronous window exists in which a second end\_turn can start a second enemy phase; a repeated call returns NOT\_PLAYER\_TURN.

### 9.3 Turn order (CMB-03, documented and fixed)

**Combat setup.** (1) Build the draw pile from the run deck and shuffle with the combat RNG. (2) Initialize player HP from the run. (3) Apply modifiers: START\_BLOCK, COMBAT\_START\_HP\_LOSS (HP never below 1), COMBAT\_START\_STATUS. (4) Initialize enemy HP and hostility rules (§14.4, informer flag). (5) Apply phase 0 entry effects and choose the first intent. (6) Begin player turn 1.

**Player turn start.**

1. turn\_number increases; turn trackers reset.
2. Block: on turn 2 and later, block = min(block, Unshakable Stance amount, or 0 if none). On turn 1 the starting Block is kept.
3. Energy = max\_energy + next\_turn\_energy; next\_turn\_energy resets to 0; then the turn-1 trait adjustment, then Qi Disruption (−1, consumed); clamp to 0 through ENERGY\_CAP (10).
4. Draw COMBAT\_DRAW\_PER\_TURN (5), plus FIRST\_TURN\_DRAW\_ADD on turn 1.
5. The slice defines no other start-of-turn effects. None are stubbed.

**End of turn (player presses End Turn).**

1. Internalize converts unspent Energy to Block.
2. Hand cleanup: Retain cards stay, every other card goes to discard. Cards with end-turn effects (Meridian Strain) resolve first.
3. Phase becomes ENEMY\_TURN.

**Enemy phase.**

1. Enemy Block clears (down to its Unshakable Stance amount, if any).
2. If the enemy has Internal Bleeding, it takes its stacks as damage that ignores Block. If it dies, its intent does not resolve.
3. The enemy resolves exactly the intent that was displayed (§9.6 pipeline).
4. **Round end:** Weak and Vulnerable lose 1; Internal Bleeding loses 1 stack; just\_applied flags clear. A status applied during the enemy phase carries just\_applied and skips this one decrement, so debuffs an enemy places on you last through your next turn. Statuses at zero are removed.
5. A pending boss phase shift takes effect (§11.3), then the next intent is chosen and shown.
6. If no terminal state was reached, PLAYER\_TURN begins. Terminal checks run after every atomic effect.

### 9.4 Energy (CMB-04)

Base 3 Energy per turn (COMBAT\_BASE\_ENERGY). Unspent Energy is lost, except through Internalize or next\_turn\_energy. ENERGY\_CAP is 10. The Energy orb shows current, max, and “+N next turn” when next\_turn\_energy is above zero.

Effective cost = base (or upgraded) cost, plus the Heavy Hands modifier for strike-tagged cards on turn 1, never below 0. Blood Price cards cost no Energy and ignore every Energy-cost modifier. Unplayable cards cannot be played. A card is playable only when: phase is PLAYER\_TURN; the card is in hand; Energy is at least its effective cost; and, for Blood Price cards, HP is greater than the price. Cost is computed on demand and never written back into the card.

### 9.5 Status effects (the complete list of 10)

| Status | Who | Stacking | Effect | Ends |
| --- | --- | --- | --- | --- |
| Weak | Both | Duration adds | Attacker deals 75% damage (rounded down) | −1 at round end |
| Vulnerable | Both | Duration adds | Defender takes 150% damage (rounded down) | −1 at round end |
| Qi Disruption | Both | Does not stack (1) | Player: next turn starts with 1 less Energy. Enemy: its next multi-hit or Special intent deals 70% damage | Consumed when it takes effect |
| Internal Bleeding | Both | Stacks add (cap 20) | Each time the afflicted acts, it loses HP equal to the stacks, ignoring Block. Enemy: when it acts. Player: when it plays an Attack card | −1 stack at round end |
| Sword Intent | Player | Stacks add | The next sword-tagged Attack deals +X on its first hit | Consumed after that attack |
| Unshakable Stance | Both | Stacks add (cap 30) | At turn start, keep up to X Block instead of losing all of it | Lasts the combat |
| Strength | Both | Stacks add | +X flat damage on every attack hit | Lasts the combat |
| Severed | Both | Stacks add | The afflicted’s next Attack deals X less damage per hit (minimum 0) | Consumed when it attacks |
| Evade | Player | Stacks add | Negates the next X hits against you | Expires at your next turn start |
| Internalize | Player | Stacks add | At end of turn, each unspent Energy becomes X Block | Cleared after conversion |

### 9.6 Damage pipeline (CMB-05, integer math, every step rounds down)

For each hit, in this order:

1. flat = base + attacker Strength + Sword Intent (first hit of a sword-tagged Attack only) − attacker Severed; floor at 0.
2. Attacker Qi Disruption on a qualifying enemy intent: × 70 ÷ 100.
3. Attacker Weak: × 75 ÷ 100.
4. Defender Vulnerable: × 150 ÷ 100.
5. Defender Evade of 1 or more: the hit is negated and Evade drops by 1; stop.
6. Block absorbs: absorbed = min(block, damage); the rest is HP loss.
7. Drain heals the attacker by the HP actually lost by the target, up to the card’s cap, plus any perk bonus.
8. Events are appended and terminal state is checked.

HP loss from Blood Price, Bleeding or card costs is not damage: it ignores Block, Vulnerable and Evade. Intent previews call the same function with no side effects and refresh whenever any status or stat changes, so a displayed number always equals the resolved number. Tie rule: if both sides reach 0 inside one effect, the result is DEFEAT.

### 9.7 Keywords (the single glossary the text builder uses)

| Keyword | Reminder text |
| --- | --- |
| Form | If the previous card you played this turn was an Attack, \[effect\]. |
| Internalize \[X\] | Each unspent Energy becomes \[X\] Block at the end of your turn. |
| Blood Price \[X\] | Lose \[X\] HP to play this. It costs no Energy. Needs more than \[X\] HP. |
| Severance \[X\] | The target’s next attack deals \[X\] less damage. |
| Drain \[X\] | Heal for HP damage dealt, up to \[X\]. |
| Evade \[X\] | Negate the next \[X\] hits against you. Ends when your next turn starts. |
| Retain | Not discarded at end of turn. |
| Exhaust | Removed from play for the rest of this combat. |

### 9.8 Card lifecycle and guards (CMB-06)

- **Draw.** For each card: if hand size is 10 (HAND\_MAX), the card is burned to discard. If the draw pile is empty, shuffle the discard pile into a new draw pile with the combat RNG (Fisher–Yates). If both piles are empty, drawing stops with no loop. The exhaust pile never reshuffles.
- **Play.** Validate; remove from hand; pay the cost; resolve effects in listed order; then move the card: Exhaust flag to the exhaust pile, otherwise to discard.
- **Upgrade.** An upgraded instance uses upgrade\_effects when present, and the upgrade cost overrides. Nothing is mutated on CardData.
- **Guards.** At most COMBAT\_MAX\_CARDS\_PER\_TURN (40) plays per turn; at most COMBAT\_MAX\_DRAW\_PER\_EFFECT (10); Block capped at BLOCK\_CAP (99); DOUBLE\_BLOCK adds at most BLOCK\_DOUBLE\_MAX\_GAIN (30).
- **Status cards.** Cards added by enemies during combat enter the discard pile for that combat only. Cards added by events go to the run deck.
- **Terminal latch.** Once the outcome is not ONGOING, every action returns COMBAT\_OVER, remaining effects of the current action are dropped, and Victory and Defeat can never both fire.

### 9.9 Event log, presenter and input gate (CMB-07)

Every state change appends a CombatEvent in order. Types: TURN\_STARTED, CARD\_DRAWN, CARD\_BURNED, DECK\_RESHUFFLED, CARD\_PLAYED, DAMAGE\_DEALT, HIT\_EVADED, BLOCK\_GAINED, HP\_LOST, HEALED, ENERGY\_CHANGED, STATUS\_APPLIED, STATUS\_EXPIRED, INTENT\_REVEALED, ENEMY\_ACTED, PHASE\_SHIFT, COMBAT\_ENDED.

The engine resolves a whole action instantly. The presenter plays the events with tweens (timings in GameConfig UI\_), supports tap-to-skip, and after playback re-renders from CombatState. While playback runs, cards and End Turn show a disabled state; the engine would reject duplicates anyway. Leaving the scene mid-animation never changes state.

**Playing a card by touch.** Tap a card to select it (it lifts and the inspection panel shows its full text and live numbers). Tap the selected card again, or tap the enemy for targeted cards, to play it. Tapping elsewhere deselects. Dragging up is an optional enhancement, never the only way.

### 9.10 Result

On a terminal state the scene builds one CombatResult (combat\_id, outcome, final HP, turns) and hands it to RunSession, which applies it once per combat\_id.

---

## 10. Card Catalogue (content lock: 24 cards plus 1 status card)

Rarity and style follow §6.2. “Form” lines are effects with condition PREV\_CARD\_ATTACK. The Job column is the design purpose stored in CardData.job. Orthodox Archive cards require the profile flag orthodox\_archive\_1.

### 10.1 Starter and Neutral (Formless Wanderers)

| Card (style, faction, rarity) | Cost and type | Base | Upgraded | Job |
| --- | --- | --- | --- | --- |
| straight\_cut\_sword, Straight-Cut Sword (Sword, Starter) | 1, Attack; tags strike, sword | Deal 6 | Deal 9 | Reliable damage; the baseline everything else is measured against |
| iron\_shirt, Iron Shirt (Body, Starter) | 1, Technique | Gain 5 Block | Gain 8 Block | Reliable defense |
| gathering\_breath, Gathering Breath (Internal, Starter) | 0, Technique; Exhaust | +1 Energy next turn | +1 Energy next turn and gain 3 Block | Trade a card for tempo; teaches Energy planning |
| drifting\_leaf\_step, Drifting Leaf Step (Movement, Neutral, Common) | 1, Technique | Evade 1. Draw 1 | Evade 1. Draw 1. Gain 3 Block | Answers one announced hit while cycling |
| idle\_wind, Idle Wind (Movement, Neutral, Common) | 0, Technique; Exhaust | Discard your hand, then draw that many cards plus 1 | Draw that many plus 2 | Rewrites a bad hand once per combat |
| flowing\_water\_palm, Flowing Water Palm (Fist, Neutral, Common) | 1, Attack; tag fist | Deal 5. Form: draw 1 | Deal 7. Form: draw 1 | Rewards chaining after another Attack with card flow |
| meridian\_severance, Meridian Severance (Fist, Neutral, Uncommon) | 1, Attack; tag fist | Deal 4. Severance 4 | Deal 6. Severance 5 | Blunts a telegraphed heavy hit through damage rather than Block |
| shadowless\_step, Shadowless Step (Movement, Neutral, Uncommon) | 1, Technique | Evade 2 | Evade 3 | Counters multi-hit intents and single heavy hits |
| wind\_splitting\_draw, Wind-Splitting Draw (Sword, Neutral, Uncommon) | 1, Attack; tag sword | Deal 7. Form: Sword Intent 2 | Deal 9. Form: Sword Intent 3 | Builds a sword chain: the next sword attack hits harder |

### 10.2 Orthodox (Iron Principle), available from the start

| Card | Cost and type | Base | Upgraded | Job |
| --- | --- | --- | --- | --- |
| returning\_crane, Returning Crane (Sword, Uncommon) | 1, Attack; tag sword | Deal 5. If you have Block, deal 5 more | Deal 6. If you have Block, deal 6 more | Rewards defending first, then striking |
| unmoving\_mountain, Unmoving Mountain (Body, Common) | 1, Stance | Gain 4 Block and Unshakable Stance 6 | Gain 6 Block and Stance 9 | Carries Block across turns to set up counters |
| disciplined\_breath, Disciplined Breath (Internal, Common) | 0, Technique | Internalize 2 | Internalize 3 | Turns a deliberately unspent turn into Block |
| mountain\_shattering\_fist, Mountain-Shattering Fist (Fist, Rare) | 3, Attack; tag fist; Retain | Deal 22 | Deal 28 | A turn-defining heavy hit that must be saved for |
| oath\_of\_the\_iron\_gate, Oath of the Iron Gate (Body, Uncommon) | 2, Technique; Retain | Gain 13 Block | Gain 18 Block | Holds a large Block for the exact turn a finisher lands |

### 10.3 Orthodox Archive (locked until the 150 SF unlock)

| Card | Cost and type | Base | Upgraded | Job |
| --- | --- | --- | --- | --- |
| principled\_rebuke, Principled Rebuke (Sword, Uncommon) | 1, Attack; tag sword | Deal damage equal to your Block, up to 18 | Up to 24 | Turns a defensive turn into the counterattack |
| heaven\_holding\_palm, Heaven-Holding Palm (Fist, Uncommon) | 2, Attack; tag fist | Deal 9. Gain 6 Block | Deal 12. Gain 8 Block | Efficient two-purpose play for steady turns |
| gate\_unbroken, The Gate Unbroken (Body, Rare) | 2, Technique; Retain; Exhaust | Double your Block (gain at most 30) | Cost 1 | Payoff for stacked Block |
| twin\_blade\_formation, Twin-Blade Formation (Sword, Uncommon) | 1, Attack; tag sword | Deal 5. Form: deal 5 again | Deal 7. Form: deal 7 again | Rewards sequencing as the second Attack |
| elders\_discipline, Elder’s Discipline (Internal, Rare) | 0, Technique; Retain; Exhaust | Gain 1 Energy | Gain 2 Energy | Stores Energy for a heavy turn |

### 10.4 Demonic (Crimson Marrow Cult)

| Card | Cost and type | Base | Upgraded | Job |
| --- | --- | --- | --- | --- |
| borrowed\_vitality, Borrowed Vitality (Body, Uncommon) | 1, Attack | Deal 6. Drain 6 | Deal 8. Drain 8 | Sustain that only works by hitting through Block |
| blood\_burning\_palm, Blood-Burning Palm (Forbidden, Rare) | Blood Price 6, Attack; tag fist | Deal 18 | Deal 22, Blood Price 5 | Burst damage paid in HP, stacking on top of a full Energy turn |
| severed\_meridian, Severed Meridian (Fist, Uncommon) | 1, Attack; tag fist | Deal 6. If the target has Internal Bleeding, deal 6 more | Deal 8, 8 more | Payoff for Marrow Needle |
| marrow\_needle, Marrow Needle (Forbidden, Common) | Blood Price 2, Technique | Apply Internal Bleeding 4 | Bleeding 6 | Cheap setup for damage over time |
| rite\_of\_hollow\_heartbeat, Rite of the Hollow Heartbeat (Forbidden, Rare) | Blood Price 4, Technique; Exhaust | Gain 2 Energy | Blood Price 3 | Trades HP for tempo, once per combat |

### 10.5 Status card and starter deck

- **meridian\_strain, Meridian Strain** (Status, unplayable). End-turn effect while in hand: lose 2 HP. Sources: event E4 (run deck, persistent) and the Crimson Marrow Cultivator (combat only). Removal: rest-site Treat Injury, merchant card removal, or the event options that say so.
- **Starter deck order (fixed):** Straight-Cut Sword ×5, Iron Shirt ×4, Gathering Breath. Total 10 cards.

### 10.6 Reward rules and archetype coverage

Reward pool = cards with rarity not Starter and not Status, whose unlock\_flag is owned, weighted by the band table in §7.4. Rarity weights (tunable): standard fight Common 60 / Uncommon 33 / Rare 7; elite 35 / 45 / 20 with at least one Uncommon or better; merchants per §13.4. Archetypes the pool MUST support, each with at least four relevant cards: **steady attack and defense** (Sword, Iron Shirt, Heaven-Holding Palm); **heavy hitters** (Mountain-Shattering Fist, Blood-Burning Palm, Elder’s Discipline); **defensive counter** (Unmoving Mountain, Oath of the Iron Gate, Principled Rebuke, The Gate Unbroken); **Energy and draw** (Gathering Breath, Drifting Leaf Step, Idle Wind, Elder’s Discipline); **forbidden gamble** (Marrow Needle, Severed Meridian, Borrowed Vitality, Rite of the Hollow Heartbeat). A test counts these.

---

## 11. Enemies, Elites and the Boss

### 11.1 Roster (content lock: 3 standard, 2 elite, 1 boss)

Every intent shows kind, a plain-language tell, and live numbers from the §9.6 pipeline. A tell is one short sentence such as “Winds up a heavy strike.”

| Enemy | Tier and faction | HP | Gold | Intents (weight) |
| --- | --- | --- | --- | --- |
| roadside\_bandit, Roadside Bandit | Standard, unaffiliated | 36 | 12–20 | Strike (Attack 8; 50). Guard (Defend, 6 Block; 30). Taunt (Buff, Strength +2; 20) |
| iron\_fist\_disciple, Iron-Fist Disciple | Standard, Iron Principle | 46 | 12–20 | Rapid Palms (Attack 4 × 2; 40). Iron Fist (Attack 11; 30). Pressure-Point Jab (Debuff: 5 damage and Qi Disruption on you; 15). Settle the Stance (Buff: 6 Block and Strength +1; 15) |
| wandering\_swordsman, Wandering Swordsman | Standard, Formless Wanderers | 42 | 12–20 | Starts Closed. Closed: Reading the Opening (Defend, 8 Block, sets Open; 50), Probing Cut (Attack 7; 50). Open: Flowing Cut (Attack 13; 55), Double Step (Attack 5 × 2; 25), Close the Guard (Defend, 6 Block, sets Closed; 20) |
| orthodox\_enforcer, Orthodox Enforcer | Elite, Iron Principle | 78 | 30–45 | Starts Ready. Ready: Measured Strike (Attack 10; 40), Hold the Line (Defend, 12 Block, sets Braced; 30), Decree of Obedience (Debuff: Weak 2; 30). Braced: Righteous Reprisal (Attack 20, sets Ready; 100) |
| crimson\_marrow\_cultivator, Crimson Marrow Cultivator | Elite, Crimson Marrow | 70 | 30–45 | Hungry Palm (Attack 8 with Drain 4; 35). Marrow Needle (Debuff: 3 damage and Internal Bleeding 3 on you; 20). Blood Offering (Buff: loses 6 HP, gains Strength +3; 25). Tainted Draught (Special: 5 damage and a Meridian Strain in your discard pile; 20) |
| hall\_master\_gwak, Hall-Master Gwak Yeon-seok | Boss, Iron Principle (Blackwater Branch) | 160 | none | Scripted, §11.3 |

Design intent: the Bandit teaches Block timing and Strength growth; the Disciple teaches multi-hit and Qi Disruption; the Swordsman teaches reading a stance; the Enforcer teaches that a Block telegraph means a big hit is coming; the Cultivator teaches Bleeding and unwanted cards; the boss tests all of it.

### 11.2 Intent selection (AI-01)

1. If the current phase has a sequence, take the next entry (looping). Otherwise continue.
2. Candidates are the phase’s intents whose requires\_stance matches the enemy’s current stance (or has none).
3. Remove any intent already chosen max\_consecutive times in a row (default 2). If that empties the list, ignore this step so selection never fails.
4. Remove any intent whose self-HP cost would drop the enemy below 1 HP.
5. Pick by weight with the combat RNG. Store the pick as the displayed intent.

The displayed intent is resolved as shown; it is never re-rolled. sets\_stance is applied when the intent resolves. Intent previews recompute live from the pipeline when Strength, Weak, Vulnerable, Severed or Block change. Tapping an intent opens a one-line explanation plus the numbers.

### 11.3 Boss: Hall-Master Gwak Yeon-seok (BOSS-01)

A disciplined sword master who taxes the pass for its own protection. The fight tests Block timing, Energy planning for a heavy answer, and reading a tell.

| Intent | Kind | Numbers |
| --- | --- | --- |
| Measured Cut | Attack | 12 |
| Tax Decree | Debuff | 6 damage and Weak 2 on you |
| Gate Guard | Defend | 14 Block |
| Verdict Charge | Buff (telegraph) | 8 Block. Tell: “The next strike is the verdict.” |
| Verdict | Special (Attack) | 30 |
| Double Cut | Attack | 8 × 2 |
| Final Verdict | Special (Attack) | 34 |

- **Phase 1** (enters at 100% HP): sequence Measured Cut → Tax Decree → Gate Guard → Verdict Charge → Verdict, looping.
- **Phase 2** (enter\_at\_hp\_pct 50): entry effects once: Strength +2 and 10 Block. Sequence Double Cut → Tax Decree → Verdict Charge → Final Verdict, looping.
- **Phase shift rules.** When HP first drops to 50% or below, pending\_phase is set once and compared by phase index, so healing or further damage can never retrigger it. The currently displayed intent is never replaced. While the current intent is a telegraph (Verdict Charge), the shift is deferred until the Verdict it announced has resolved. Then PHASE\_SHIFT fires once, entry effects apply once, sequence\_index resets, and the first phase 2 intent is chosen and shown.
- **Victory** ends the run as a clear: Blackwater Pass is passed (§15).

### 11.4 Balance baselines and the simulation harness (BAL-01)

Starter turn math: a five-card hand with 3 Energy yields about 12–14 damage when mixing Strikes and Block, so the Bandit (36 HP) falls in about three turns while dealing roughly 15 HP of damage to an unprepared player. Pacing target: a typical run reaches the boss with 55–65% of max HP after three fights, one elite and one rest.

tests/sim\_combat.gd runs a greedy bot (play the highest value affordable card; block when the intent is lethal) over at least 200 seeds per matchup and prints a table. Targets with the bot, which plays worse than a human:

| Matchup | Win rate target | Average HP lost |
| --- | --- | --- |
| Starter deck vs Roadside Bandit | 90% or more | 8–18 |
| Starter deck vs Iron-Fist Disciple | 80% or more | 12–24 |
| Starter deck vs Wandering Swordsman | 85% or more | 10–20 |
| Starter plus three rewards vs either elite | 55% or more | 20–35 |
| Starter plus eight rewards and two upgrades vs boss | 40% or more | 45–75 |

If a matchup misses its target, adjust tunable numbers only (enemy HP and damage, card values) and record the change in DECISIONS.md. Results are reported with RAN evidence or not at all.

---

## 12. The Expedition Map

### 12.1 Structure (MAP-01)

Five floors plus a boss floor, **10 nodes**, generated once per run from the map RNG stream.

| Floor | Nodes | Allowed types |
| --- | --- | --- |
| 1 | 2 | Regular enemy, both |
| 2 | 2 | Regular enemy 45, Event 35, Treasure (manual discovery) 20; at least one is not a regular enemy |
| 3 | 2 | Elite 30, Merchant 25, Event 25, Regular enemy 20 |
| 4 | 2 | Regular enemy, Event, Merchant, Treasure, Elite |
| 5 | 1 | Rest site (guaranteed) |
| 6 | 1 | Boss |

Generation rules, all validated by tests:

1. Each node connects to one or two nodes on the next floor, every node has at least one incoming edge (except floor 1) and at least one outgoing edge (except the boss), and each floor pair has at most one crossing edge.
2. Floors 3–4 together contain exactly one Elite and at least one Merchant.
3. Every path from floor 1 to the boss contains at least two combat nodes (regular or elite).
4. Events within a map never repeat an event id. Combat nodes never repeat the same enemy on adjacent floors.
5. A failed validation retries with the next value of the map RNG, up to 50 attempts, then falls back to a fixed template layout documented in game\_config.gd. Generation never loops forever and never produces an unreachable boss.

### 12.2 Node previews (MAP-02)

Tapping an available node opens a bottom sheet with its icon, a type word, and a one-line risk and reward. Combat nodes name the enemy and tier (enemies are chosen at generation time, so route choice is informed). Events say Event with no detail. Treasure says: choose one of three rare techniques. Merchant, Rest and Boss are labeled. The sheet has Enter and Cancel buttons at least 144 px tall.

**Treasure (manual discovery)** offers three Rare cards from the player’s accessible pool (weights per §7.4), each presented as a martial manual with one line of provenance; the player takes one or skips.

### 12.3 State and persistence (MAP-03)

MapState: seed, nodes (id, floor, index, type, enemy\_id or event\_id, state, edges), current\_node\_id. Node states: LOCKED, AVAILABLE, IN\_PROGRESS, CLEARED. Only AVAILABLE nodes can be entered. Resolving a node is idempotent: resolving a CLEARED node does nothing, so rewards cannot be duplicated. A floor counts as traversed when its node is CLEARED. The map is never regenerated; returning from a node re-renders the same state.

Autosave points: run start; node entry (snapshot before any effect); node resolved. If the app is killed mid-node, resume restores the entry snapshot and the node is AVAILABLE again; because the combat RNG is seeded from the run seed and node index, the same encounter and shuffle return.

### 12.4 Wandering Merchant swap (MAP-04)

Only when the profile flag merchant\_wanderer is owned: for each of floors 2–4 in order, with probability MAP\_WANDERER\_CHANCE (0.35) replace one regular-enemy, event or treasure node with a Wandering Merchant, at most one per map, and only if rule 3 of §12.1 still holds. It never changes node counts or edges, and it never replaces the guaranteed Merchant or Elite. Without the flag the type is never generated; a test asserts both directions.

### 12.5 Presentation (MAP-05)

A vertical travel journal: the Start at the bottom and the Boss at the top, so the thumb moves upward. Six rows fit on one 1080 × 1920 screen without scrolling (a ScrollContainer is the fallback on shorter displays). Node markers are at least 144 px with a label beneath; each uses a distinct silhouette and a word, not color alone. States: available (full ink, steady), current (red seal), cleared (stamped and dimmed), locked (faint outline). Routes are ink strokes with varying width; the traveled route is darker, unreachable routes are dashed. Behind the nodes, simple procedural landscape silhouettes (mountain pass, river crossing, abandoned temple, bandit camp, burial ground) are decorative only and never interactive. The player’s HP, Gold and deck button sit in a top bar inside the safe area.

---

## 13. Events, Rewards, Merchants and Rest

### 13.1 Combat rewards (REWARD-01)

- **Standard victory:** Gold (rolled within the enemy’s range) and a choice of three cards (four on the first reward under Open Road). The player may skip the card.
- **Elite victory:** Gold, a choice of three cards with elite rarity weights (§10.6), and a Herb Poultice that heals 12% of max HP (rounded down) if taken.
- **Treasure node:** three Rare manuals (§12.2).
- **Generation and claiming.** The reward set is rolled with the reward RNG when the combat is won, keyed by node\_id. Each item has a claimed flag. Claiming is idempotent, the Done button is disabled after one press, and a resolved node cannot be re-entered, so rewards are applied exactly once.

### 13.2 Events (content lock: 6)

Choices show their cost and benefit before selection. A choice whose requirement is unmet is disabled with the reason beside it. Outcomes apply atomically and once; the node clears when a choice resolves.

| Event | Situation | Choices and outcomes |
| --- | --- | --- |
| E1 ruined\_monastery\_manual | A burned monastery at Yeongun Pass. In the abbot’s cell lies a half-charred manual with two readable pages | Study the pages: lose 8 HP, upgrade one card of your choice. Tear out the intact page and sell it in the next town: gain 60 Gold. Rebury the manual with the abbot’s ashes and rest: heal 15% of max HP |
| E2 traitors\_bounty | Moon Ji-ho, in Iron Principle gray, lies wounded under a roadside notice offering 90 Gold for the traitor | Hide and treat him: lose 10 HP, add Drifting Leaf Step to the deck. Turn him in: gain 90 Gold and set run flag betrayed\_wanderer. Walk on: nothing changes |
| E3 qinghe\_tribute | At Qinghe Ford an Iron Principle collector loads rice sacks while villagers stand with empty bowls | Pay the tribute for them: lose 60 Gold, heal 15% of max HP. Challenge the collector (needs 40 or more HP): fight the Orthodox Enforcer, with elite rewards on victory. Hide the grain in the well: lose 12 HP, gain 50 Gold. Gated by iron\_principle\_favor: Request Instruction, upgrade one card free |
| E4 marrow\_remedy | A cart with a red lantern stands outside Dongmun. A Crimson Marrow healer offers a tincture that mends bone overnight and warns the strain will linger | Drink the tincture: heal 50% of max HP, add Meridian Strain to the deck, set run flag marrow\_pact. Gated by shielded\_marrow: accept the clinic’s care, heal 30% of max HP, no injury, set marrow\_pact. Buy a sealed jar: lose 45 Gold, heal 25% of max HP. Decline: nothing changes |
| E5 physicians\_price | A physician with a lacquered case sets bones only for payment in something other than coin | Pay with a memory: remove one card of your choice, heal 40% of max HP. Pay with years: lose 6 max HP, heal to full. Haggle in silver at triple his rate: lose 70 Gold, heal 25% of max HP |
| E6 sealed\_cave | Behind the waterfall at Cheongun Falls a cave is closed by an Iron Principle seal. Carvings inside describe a technique that reshapes an existing move | Break the seal and enter: lose 12 HP, transform one chosen card into a random card of the same style and equal or higher rarity from your accessible pool (disabled if none exists). Copy the carvings for a scribe: gain 45 Gold. Rest at the cave mouth: heal 20% of max HP |

Event selection uses the event RNG, never repeats within a run, and E3 and E4 are weighted up when their gating flags are present. All healing respects max HP. LOSE\_HP from events cannot reduce HP below 1.

### 13.3 Rest site (REST-01)

One action per site, then the node clears and cannot be reopened.

- **Recover:** heal by the §8.4 formula (baseline 30% of max HP, rounded down), limited to missing HP.
- **Upgrade:** a picker lists cards that are not upgraded, have upgrade data, and are not Status cards. If none exist the option is disabled with the reason.
- **Treat Injury:** shown only if the deck contains Meridian Strain; removes one copy.

### 13.4 Merchants (MERCH-01)

**Regular Merchant:** three cards (rarity weights Common 50 / Uncommon 40 / Rare 10, at least one from the player’s favored pool), one Wound Salve, and Card Removal. **Wandering Merchant** (meta-locked): two Uncommon and one Rare card at a 10% discount, Card Removal, and Card Exchange.

| Item | Price |
| --- | --- |
| Common / Uncommon / Rare card | 50 / 80 / 140 Gold (Wandering: 45 / 72 / 126) |
| Wound Salve | 45 Gold; heals 20% of max HP immediately, rounded down |
| Card Removal | 75 Gold, then +25 for each earlier removal in the same run (75, 100, 125…) |
| Card Exchange (Wandering only) | Free once per visit: replace a chosen card with a random card of the same rarity from the accessible pool, never the same id, never Starter or Status |

Rules: the Gold balance is always visible; an unaffordable offer is disabled and shows how much Gold is missing; a purchase gives immediate visual and haptic feedback and updates deck and Gold at once; each offer is idempotent (a purchased offer is marked sold). Leave is always visible and clears the node. Stock is rolled with the shop RNG seeded by node\_id. The removal counter persists across merchants within one run and resets for a new run.

### 13.5 Economy baseline

Starting Gold 100. Enemy Gold per §11.1. A typical run earns 120–180 Gold before the boss, enough for one card plus one removal, or a Salve and a card. Gold left at run end is lost; it has no meta value.

---

## 14. World, Factions and Paths

### 14.1 Setting (WORLD-01)

Blackwater Pass is a mountain road between Qinghe Ford and Dongmun. The Blackwater Branch of the Iron Principle holds it and collects a protection levy from everyone who travels or lives along it. The protagonist is never named and is addressed as you. Their previous life is revealed only through the Judgment. Use Murim vocabulary precisely and sparingly (Qi, meridians, dantian, sect, manual, hall); never use Dao or Heaven’s Will as filler. Names are original and Korean-romanized (for example Gwak Yeon-seok, Han Seo-jun, Moon Ji-ho). Do not name or imitate characters from any existing franchise.

### 14.2 The three factions

Every faction MUST display a virtue and a vice somewhere in the slice.

| Faction | Mechanical identity | Virtue shown | Vice shown | Offers | Demands |
| --- | --- | --- | --- | --- | --- |
| The Iron Principle (Orthodox) | Block, Retain, high-cost heavy attacks | Keeps the road passable and trains disciples | Demands obedience, taxes commoners for protection, cripples deserters | Archive cards, free upgrades (E3), a stable pool | Hostility toward those carrying Marrow arts |
| The Crimson Marrow Cult (Demonic) | Drain, Blood Price, Exhaust | Shelters orphans and the plague-sick the Orthodox call unclean | Its cures and rites cost the body; it recruits the desperate | The Demonic pool, the clinic (E4), forbidden speed | Injuries and the Iron Principle’s enmity |
| The Formless Wanderers (Neutral) | Draw, discard, Evade, stance play | Abandoned sects that demanded too much | Unreliable mercenaries who sell what they know | The flexible Neutral pool | Nothing, and they trust nobody |

### 14.3 Paths as play

- **Orthodox:** stable Block, Retain and Stance engines, free upgrades and Archive depth. Limits: heavy cards need Energy planning (Elder’s Discipline), Marrow cards are scarce until a pact, and the Enforcer punishes deviation.
- **Demonic:** Drain, Blood Price bursts, Bleeding and Exhaust tempo. Limits: HP is the real currency, Meridian Strain injuries accumulate, and Iron Principle enemies hit harder.
- **Neutral:** the widest pool, with Evade, draw and flexible Energy. Limits: no specialist payoff cards unless the player earns a pact or an archive. A neutral or unaffiliated run MUST remain viable: the Neutral pool alone supports a complete deck (§10.6 archetypes).

### 14.4 Restrictions enforced in systems (PATH-01)

Hostility is data on EnemyData.hostility\_rules (condition, count, effect). Restrictions live in logic, not only in UI:

1. Orthodox Enforcer starts combat with Strength 2 if the run deck holds two or more Demonic-faction cards.
2. Crimson Marrow Cultivator starts with Strength 2 if the run flag informer is set.
3. Wandering Swordsman starts with Strength 2 if the run flag betrayed\_wanderer is set.
4. The reward, merchant and treasure generators exclude the Demonic pool unless the band is Tainted or Asura or the run flag marrow\_pact is set.
5. Archive cards require the profile flag orthodox\_archive\_1.
6. Event options and traits check their flag and alignment requirements in logic (Request Instruction, clinic care, Blood Debt).
7. No card is ever blocked at play time. Alignment limits acquisition, enemy reactions and events, never what a player may use.

---

## 15. Death, Soul Fragments and the Reincarnation Hub

### 15.1 End of a run is a transition (DEATH-01)

On player HP 0 (or boss defeat, or Abandon Run from the map menu):

1. The terminal latch ends combat at once and all combat input is disabled.
2. Record the RunSummary: outcome, floors traversed, nodes cleared, enemies by tier, turns, Gold, deck ids, traits, band, seed code, and the cause (enemy name and last intent name, or Abandoned).
3. Settle Soul Fragments from the ledger. Settlement is idempotent (RunState.settled).
4. Update Profile (balance, lifetime total, stats, last\_run\_summary) and write it with the atomic protocol of §16.3. Only after the write is verified, delete the run save.
5. Show the screen: one cause line; what was accomplished; the Soul Fragment breakdown with a skippable count-up; one band-specific closing line from Heaven (at least three variants); the seed code. A single Continue button (at least 144 px tall) leads to the Hub. A boss victory uses the same screen with a cleared-pass headline.
6. Starting the next life creates a fresh RunState. Nothing temporary (deck, flags, ledger, Gold, HP, map, RNG state) carries over; a test compares a new run against a clean default.

Tone: one sentence of cause, no melodrama, no motivational filler.

### 15.2 Soul Fragment ledger (SOUL-01)

| Source | Amount | Counted |
| --- | --- | --- |
| Regular enemy victory | 5 | Once per combat\_id |
| Elite enemy victory | 20 | Once per combat\_id |
| Boss victory | 100 | Once per run |
| Floor traversed | 10 per floor | Once per floor number, when that floor’s node is cleared |

The ledger is a list of entries (source, key, amount) in RunState; adding an entry with an existing key is ignored. The total is capped at SOUL\_RUN\_CAP (1000) and can never be negative. Examples: dying on floor 3 after clearing floors 1–2 with two regular wins gives 20 + 10 = 30. A full clear with three regular wins, one elite and the boss gives 60 + 15 + 20 + 100 = 195. The four unlocks total 1,000, so the first is reachable in roughly two short runs and the full set in about ten. Amounts are tunable in GameConfig; do not tune by adding sources.

### 15.3 The Hub (HUB-01)

Top: Soul Fragment balance. Then a Previous Life card (outcome, floors, cause, fragments gained, seed code). Then the four unlock cards, each with name, cost, one-line effect, and a state: Owned, Available, or Short by N. At the bottom, in the thumb zone: Begin Next Life (primary) and Settings.

Purchase flow: tap an unlock, a confirmation sheet shows cost and effect, Confirm validates (not owned, balance at least the cost, requirements met), then atomically deducts the cost, records the unlock id, adds its flags, and writes the Profile with the verified protocol. If the write fails, memory is rolled back and an error is shown. The Confirm button disables after the first tap. Locked or already-owned content can never be bought.

### 15.4 The four unlocks (content lock)

| Unlock id | Cost | Flag granted | What changes in the game |
| --- | --- | --- | --- |
| wandering\_merchant | 50 | merchant\_wanderer | Map generation can place a Wandering Merchant (§12.4, §13.4) |
| orthodox\_archive | 150 | orthodox\_archive\_1 | Five Archive cards join reward, merchant and treasure pools (§10.3) |
| heavenly\_body | 300 | trait\_heavenly\_body | Heavenly Body appears as selectable in trait selection (§8.3) |
| heavens\_memory | 500 | unlocked\_past\_betrayal | Gated Judgment choices appear (§7.5), the Cynic route opens, Remembered Blade becomes obtainable (§7.6) and Heaven speaks its memory line |

Profile.unlocked\_flags is an Array\[String\], deduplicated and validated against KNOWN\_FLAGS. Judgment and events read it through one function, Profile.has\_flag(flag). Post-slice unlocks follow the same pattern: an unlock injects flags, and content checks flags (§21).

---

## 16. Save System and Data Safety

### 16.1 Principles (SAVE-00)

Offline only. Two files in user://: profile.json (permanent) and run.json (the active run). Each has a .bak sibling. JSON only (SEC-02). Every file carries schema\_version. Permanent and temporary data never share a file. Save triggers: after a purchase, after run settlement, after a settings change, at the run autosave points (§12.3), and when the app is paused or asked to close (NOTIFICATION\_APPLICATION\_PAUSED, NOTIFICATION\_WM\_CLOSE\_REQUEST), because mobile apps can be killed without warning.

### 16.2 Profile schema, version 1

Envelope example:

```
{
  "schema_version": 1,
  "saved_unix": 1790000000,
  "profile": {
    "soul_fragments": 120,
    "purchased_unlocks": ["wandering_merchant"],
    "unlocked_flags": ["merchant_wanderer"]
  }
}
```

| Field | Type and bounds | Default |
| --- | --- | --- |
| soul\_fragments | int, 0 to 1,000,000 | 0 |
| lifetime\_soul\_fragments | int, 0 to 100,000,000 | 0 |
| purchased\_unlocks | Array\[String\], ids that exist in Content, no duplicates | empty |
| unlocked\_flags | Array\[String\], members of KNOWN\_FLAGS, at most 256 | empty |
| stats | runs\_started, runs\_ended, deaths, bosses\_defeated, elites\_defeated, best\_floor (ints at 0 or above) | zeros |
| last\_run\_summary | validated subset of RunSummary, or empty | empty |
| settings | text\_scale (0–2), reduce\_motion, haptics, high\_contrast, confirm\_end\_turn (bools), master, music, sfx volumes (0.0–1.0) | sensible defaults |
| seen\_hints | Array\[String\], at most 64 entries of 64 characters | empty |

### 16.3 Write protocol (SAVE-01)

1. Serialize with JSON.stringify and reject anything over SAVE\_MAX\_BYTES (1 MB).
2. Open name.tmp for writing; check FileAccess.get\_open\_error(); store the text; check get\_error(); close.
3. Re-open the tmp file, parse it with a JSON instance (check the returned Error), and run the validator. On any failure delete the tmp file, report the error, and leave existing files untouched.
4. If name exists: delete the old .bak, then rename name to name.bak.
5. Rename name.tmp to name and check the Error. If it fails, rename the .bak back.
6. Return an Error code to the caller. Callers surface failures; they never ignore them.

### 16.4 Load and recovery (SAVE-02)

Order: primary, then .bak, then defaults.

- A file over the size cap, unparseable, not a Dictionary, or missing schema\_version is treated as corrupt: rename it to name.corrupt-UNIX.json (keep at most three) and try the next source.
- **schema\_version above the current version:** do not load, do not overwrite. Run the session on defaults in read-only mode and tell the player that the save is from a newer version.
- **Older version:** migrate step by step (§16.6), then validate.
- **Validation:** strict types; integers accepted from floats only if integral; unknown keys dropped; unknown ids dropped with a logged warning; numbers clamped; arrays capped and deduplicated; strings capped at 64 characters; unlocked\_flags re-derived so it always includes the grants of every purchased unlock (self-healing).
- **Notices:** restoring from backup shows a non-blocking message; starting fresh after total failure shows one too. Nothing is reset silently, and the app never crashes on a bad save.
- Currency is clamped to zero on load and spending is validated before deduction, so a negative balance cannot exist.

### 16.5 Run save and resume (RUNSAVE-01)

run.json stores: seed, RNG stream states (as strings), content\_version, JudgmentResult, trait ids, deck (instance id, data id, is\_upgraded), HP, max HP, Gold, run flags, map (nodes, edges, states), soul ledger, removals\_this\_run, and the current node. It never stores combat state, reward screens or UI.

On boot, a valid run whose content\_version matches the build shows Resume Run (primary) and Abandon Run (secondary; settles the ledger) in the Hub. A version mismatch abandons the run automatically with a notice and settles its ledger, so the player is not punished. A corrupt run file is quarantined with a notice. The run file is deleted only after the settlement write is verified.

### 16.6 Migrations and fixtures

migrations.gd holds an ordered list of pure functions, one per version step. tests/fixtures/saves/ holds: valid v1, truncated, malformed JSON, wrong types, negative currency, unknown ids, oversize arrays, future version, missing file, backup-only. Each has a test.

### 16.7 Honesty (SAVE-03)

Save files are plain, editable JSON. Never claim encryption, anti-cheat or tamper protection in code, UI or store copy (SEC-06).

---

## 17. Mobile UI and Accessibility

### 17.1 Layout principles (UI-01)

Reference 1080 × 1920, portrait. Every screen is a full-rect Control built from containers and anchors: Header, flexible Body, Footer. A SafeAreaContainer (a MarginContainer that reads DisplayServer.get\_display\_safe\_area(), converts it to viewport coordinates, and re-applies on size change) wraps every screen. The Footer keeps a bottom margin of at least max(safe-area inset, 24 px). Primary actions sit in the bottom 40% of the screen. Body content scrolls when it does not fit. Test viewports: 1080 × 1920, 1080 × 2400, 1440 × 3120, 750 × 1334 and 1536 × 2048 (tablet portrait).

### 17.2 Sizes (UI-02)

On a typical phone, 48 dp is about 144 reference px (§1 row 9).

| Element | Minimum | Preferred |
| --- | --- | --- |
| Touch target | 132 × 132 px | 144 × 144 px |
| Gap between adjacent targets | 16 px | 24 px |
| Body text | 36 px | 40 px |
| Secondary text | 30 px (hard floor for any text) | 34 px |
| Key numbers (HP, Energy, damage) | 48 px | 56 px or more |
| Titles | 56 px | 64 px |

Contrast: 4.5:1 for body text, 3:1 for large text and icons. A text scale setting (100%, 115%, 130%) multiplies every size; layouts MUST survive 130%.

### 17.3 Combat layout (UI-03)

Zones are percentages of the safe-area height, so they adapt to any aspect ratio.

| Zone | Share | Contents |
| --- | --- | --- |
| Top bar | 0–6% | Menu button, Gold, deck button |
| Enemy | 6–38% | Portrait, name, HP bar with the numbers always written, Block, status row, and the intent banner as the largest element: glyph, number, tell line |
| Message strip | 38–50% | Turn number, prompts such as “Choose a target”, floating numbers |
| Player | 50–62% | HP bar with numbers, Block, statuses, Energy orb (current, max, and +N next turn), pile buttons Draw, Discard, Exhaust with counts (tap opens a read-only list) |
| Inspection panel | 62–72% | Full text of the selected card with live numbers and keyword reminders; when nothing is selected, the explanation of the enemy intent |
| Hand tray | 72–92% | Horizontal ScrollContainer of compact cards (about 240 × 340 px) showing four fully and the edge of a fifth; scrolls to keep the selected card visible |
| Bottom bar | 92–100% | End Turn button, at least 240 × 144 px, bottom right, separated from the hand by at least 24 px |

Priority order is therefore survival state, enemy intent, Energy, hand, End Turn, secondary information. A compact card shows the cost badge, name, a type glyph with letter, and one short effect line; the inspection panel shows everything else. Cards that cannot be played are dimmed and, when selected, state the reason: Needs 2 Energy, Needs more than 6 HP, Unplayable. The optional setting Confirm End Turn adds a prompt when playable cards and Energy remain.

### 17.4 Other screens and navigation

- **Judgment, Event:** scrollable text, choice buttons in the bottom half.
- **Trait selection:** sticky four-number header, scrolling category sections, Confirm at the bottom.
- **Reward:** three compact cards, tap to read the full text, Take and Skip buttons.
- **Merchant:** rows at least 144 px tall, Gold always visible, Leave always visible.
- **Rest:** three large buttons, with the reason shown for any disabled one.
- **Hub, Map, Death:** as specified in §15 and §12.5.
- **Modals** always have a visible Close or Cancel and are dismissed by the Android back gesture. Set application/config/quit\_on\_go\_back to false. The Router handles go-back: close the top modal; in combat open the pause menu; at the Hub do nothing special.
- **Transitions:** one Router, a 180 ms fade, input blocked while transitioning, no duplicate scene instances.

### 17.5 Settings and accessibility (UI-04)

Settings (scrollable, saved in Profile.settings): text size, Reduce Motion, Haptics, three volume sliders, High Contrast, Confirm End Turn. **Reduce Motion** replaces movement with instant state changes or fades of 100 ms or less and disables shake, hit-stop and particles. **High Contrast** raises ink contrast and removes paper grain. Color is never the sole carrier of meaning (§5.3).

### 17.6 Localization readiness (UI-05)

All player-facing strings go through tr(). Sentences are never built by concatenation; use format placeholders so word order can change. Labels autowrap and have minimum sizes, never fixed widths. QA runs with pseudolocalization on (about 40% longer strings) and fixes any clipping. Only English ships in the slice.

---

## 18. Art Direction, Juice and Audio

### 18.1 Visual language

Traditional ink painting, weathered martial manuals, mountain landscapes, worn parchment, carved seals, dark lacquer and restrained vermilion. Original work only.

| Token | Hex | Use |
| --- | --- | --- |
| ink | #15110E | Primary text on paper, deep backgrounds |
| lacquer | #231B17 | Combat and hub backgrounds |
| lacquer\_light | #342823 | Raised surfaces on lacquer |
| parchment | #E9DDC2 | Paper surfaces |
| aged\_paper | #D2C29E | Secondary paper, dividers |
| ash | #8B8272 | Disabled and secondary text |
| vermilion | #B2362A | Primary action and danger only |
| slate\_jade | #4E6A63 | Iron Principle marks |
| marrow | #7C2230 | Crimson Marrow marks |
| wander\_green | #7D8467 | Formless Wanderer marks |
| ochre | #B8923A | Energy only |

Compose with negative space, one focal point per screen, paper grain from a baked NoiseTexture2D, and ink-wash mountain silhouettes at the screen edges. Seals (square red stamps) mark state. The only gradient allowed is an ink-wash falloff from dark to transparent.

### 18.2 Rendering rules (ART-01)

- The default Nearest filter serves pixel and bitmap art. Set texture\_filter to Linear on SVG icons, vector drawing, downscaled illustrations, and any text-heavy control that looks soft on a device. Verify at three screen densities.
- Import SVGs with a scale that makes their raster size twice their display size. Do not use unsupported SVG features (filters).
- Procedural art (mountains, brush strokes) is drawn once, baked into a texture or SubViewport, and reused; it is not redrawn every frame.
- Pack icons into one atlas; do not create a unique texture per card.
- Placeholder assets are named placeholder\_ and listed in docs/ASSET\_MANIFEST.md with status (final, placeholder, procedural).

### 18.3 Typography

Two faces: a high-contrast serif for titles and a very legible face for body and numbers, with tabular figures for numerals. Only fonts present in the repository with their license files (OFL or CC0) may be referenced. Suggested candidates: Noto Serif (body) and Gowun Batang (titles). If a font cannot be obtained in the working environment, use ThemeDB.fallback\_font and record it in ASSET\_MANIFEST.md; never reference a font file that does not exist. Sizes follow §17.2.

### 18.4 Card frames (five distinct)

- **Attack:** upright tablet with a diagonal brush-slash header and sharp corners.
- **Technique:** unrolled scroll with rolled ends.
- **Stance:** carved stone stele on a base.
- **Status:** torn page with a ragged edge.
- **Blood Price:** any card with a Blood Price replaces the cost badge with a vermilion seal that shows the HP number.

A small faction seal and a word sit at the foot of each card: gate for Orthodox, a drop of marrow for Demonic, an open circle for Neutral. Rarity is shown by one to three notches and the word. Upgraded cards show a plus mark and highlighted numbers.

### 18.5 Feedback (JUICE-01)

Every effect is driven by a combat event (§9.9), has a Reduce Motion fallback, is skippable by tap, and takes its duration from GameConfig UI\_ constants. None may delay state or allow a repeated input.

| Event | Visual | Haptic | Max time | Reduce Motion |
| --- | --- | --- | --- | --- |
| Card selected | Card lifts 24 px; inspection panel updates | 10 ms | 120 ms | Instant |
| Attack played | Card slides to the enemy with an ink trail; enemy recoils 12 px | none | 260 ms | Flash only |
| Damage dealt | Ink-splash numeral rises 40 px; 50 ms hit-stop on hits of 15 or more | 20 ms | 400 ms | Numeral only |
| Block gained | Seal stamp on the Block counter; counter ticks up | 15 ms | 250 ms | Counter change |
| Block broken | Block icon cracks | 30 ms | 200 ms | Instant |
| Healing | Jade bloom behind the HP numeral | 15 ms | 300 ms | Plus sign on numeral |
| Evade | Afterimage on the player; attack passes through | 25 ms | 250 ms | Text popup |
| Intent changed | Banner slides in; number ticks if updated | none | 150 ms | Instant |
| Damage taken | Vermilion edge flash; shake up to 6 px | 40 ms | 120 ms | Flash only |
| Boss phase shift | Ink-dark vignette and a caption | 60 ms | 900 ms | Caption only |
| Reward | Items drop onto the paper with a stamp | 15 ms | 300 ms | Instant |
| Unlock purchased | Seal stamped onto the unlock card | 40 ms | 200 ms | Instant |
| Draw | Cards slide in 60 ms apart, 400 ms total | none | 400 ms | Instant |
| Death | Ink bleeds across the screen, then settles on parchment; skippable | 80 ms | 1200 ms | Fade |

Haptics use Input.vibrate\_handheld, are gated by the Haptics setting and the platform, and never exceed 100 ms.

### 18.6 Audio

Audio is optional in the slice. If added, use only self-synthesized or CC0 sounds with license files. Buses: Master, Music, SFX, UI, each bound to its setting. Pool at most 8 AudioStreamPlayer nodes; never create players per effect. Pause audio when the app pauses. Feedback calls go through one small static helper class (Feedback) so UI scripts never touch audio or haptics directly.

---

## 19. Testing and Verification

### 19.1 Strategy (TEST-00)

The game is verified in layers: pure-logic unit tests, content validation, a combat simulation, persistence tests with fixtures, a UI layout audit, and a manual device checklist. The runner is tests/run\_tests.gd (extends SceneTree). It discovers tests/test\_*.gd files, each a RefCounted class with test\_* methods and small assert helpers, prints a summary, and calls quit(failure\_count) so the exit code reflects the result. No third-party test addon is used.

The agent MUST NOT report a test as passed unless it ran (§2.3). Anything that cannot be automated in the agent’s environment is listed with a manual procedure and marked ASSUMED.

### 19.2 Required logic tests

**Judgment (JT)**

- Every choice of every scenario can be selected and committed; the session rejects invalid transitions and a second Confirm.
- Band classification and Trait Points at the boundaries −21, −20, −1, 0, 19, 20, 49, 50 match §7.4.
- Over an exhaustive or sampled search, all five bands and both extremes (−60 to +60 range) are reachable.
- The same seed produces the same five scenarios; flag-gated choices are absent without the flag and present with it.
- Fewer than five valid scenarios triggers the recovery state, not an empty screen.

**Traits (TT)**

- Balance math and the four displayed numbers; toggling a trait on and off restores the balance exactly; a negative Remaining disables Confirm; caps and exclusions hold; locked reasons are generated.
- Applying traits twice yields the same state as applying once.
- Shattered Core gives 60 Max HP from 80. Bad Blood turns a 24 HP rest heal into 12. Meridian Prodigy gives Max Energy 4. Thick Skin gives 5 Block at combat start and never again. Heavy Hands adds 1 to strike-tagged cards on turn 1 only and not on turn 2. Weapon Master upgrades two distinct instances, and with fewer than two eligible raises no error. Blood Debt needs the Demonic class. Heavenly Body and Remembered Blade stay locked until their flags exist.

**Combat (CT)**

- Draw, reshuffle, exhaust, hand cap burn, and empty-pile behavior (no infinite loop); card counts across piles are conserved.
- Costs enforced, unaffordable cards rejected; Blood Price needs HP above the price and ignores Energy modifiers.
- Pipeline examples: 6 damage into 5 Block costs 1 HP. Base 12 from a Weak attacker into a Vulnerable defender is 9 then 13. Evade negates exactly one hit per stack. Severed reduces then is consumed. Sword Intent is consumed by the first sword-tagged Attack. Form fires only after an Attack. Internalize converts unspent Energy. Unshakable Stance retains up to X Block. Drain heals only for HP actually lost. Healing never exceeds max HP.
- Qi Disruption, Internal Bleeding timing, and just\_applied behave exactly as §9.3 and §9.5.
- Defeat interrupts the remaining enemy sequence; Victory and Defeat never both fire; a repeated end\_turn returns NOT\_PLAYER\_TURN; every action after a terminal state returns COMBAT\_OVER.
- Property test over at least 1,000 seeds: when no modifiers change in between, the damage shown in the intent equals the HP and Block actually lost.
- Guards: 40-card, draw-per-effect, Block-cap and Energy-cap limits are enforced.

**Enemies and boss (ET)**

- The consecutive-intent guard never allows a third repeat; stance gating restricts intents; sequences loop; self-HP-cost intents never drop an enemy below 1 HP.
- Boss phase shift fires exactly once, including when HP is healed back above 50% and dropped again; it defers during Verdict Charge; the displayed intent is never replaced.
- Hostility rules apply exactly as §14.4, and not otherwise.

**Map, events and economy (MT)**

- Exactly 10 nodes; every first-floor node reaches the boss (breadth-first search); every path has at least two combat nodes; exactly one Elite on floors 3–4; at least one Merchant.
- Same seed gives the same map; fallback template is valid; generation terminates.
- Unavailable nodes cannot be entered; cleared nodes stay cleared; a save and load never regenerates the map; Wandering Merchant never appears without its flag and, with the flag, never breaks the path rule.
- A table-driven test runs every choice of every event and asserts exactly the listed outcomes, requirement gating, and that no event repeats in a run.
- Removal costs 75, 100, 125; an unaffordable purchase is rejected with the missing amount; each offer is idempotent; rewards claim once.

**Meta and save (ST)**

- Ledger deduplication; the examples of §15.2 (30 and 195); settlement idempotent; Soul Fragments never negative or above the cap.
- Unlock purchase cannot duplicate, overspend or buy a locked item; each of the four unlocks changes the real game: the Wandering Merchant enters map generation, Archive cards enter reward pools, Heavenly Body becomes selectable, and the gated Judgment choices appear and affect the evaluation.
- A new run equals a clean default run (no inherited deck, flags, ledger, Gold, HP, map or RNG state).
- All fixtures in §16.6 load with the specified recovery. Failure injected between each step of the write protocol never destroys the last valid save. Integers survive the JSON round trip; 64-bit RNG state survives as a string.

**Content and slop (CST)**

- ContentValidator passes with the exact counts of §6.6. Generated text contains every effect number. The slop scan of §5 reports zero hits.

### 19.3 Restart persistence (the “close and reopen” requirement)

Automated: two separate Godot processes. Process one uses the Profile API with a test file prefix (user://test\_profile.json, never the real save) to add Soul Fragments and purchase an unlock, then exits. Process two loads and asserts the balance and the unlock. Manual on a device: earn fragments, buy an unlock, swipe the app away, reopen, and confirm both persist; then start a run and confirm the unlocked content is present.

### 19.4 Simulation and fuzzing

tests/sim\_combat.gd runs the greedy bot for the targets in §11.4 and a random-legal-action fuzzer over at least 500 seeds per enemy. Invariants: HP within bounds, Energy never negative, pile counts conserved, no exception, every combat ends within 200 turns.

### 19.5 UI layout audit

tests/ui\_layout\_audit.gd loads every screen scene into a SubViewport at each test viewport of §17.1, waits two frames, then walks the Control tree and asserts: no visible Control lies outside the viewport (excluding scrolled content); every Button and tappable Control is at least 132 × 132 px; no text is below 30 px; no script errors occurred. Run it again with text scale 130% and pseudolocalization on.

### 19.6 Manual device checklist (Android and iOS)

Cold start; notch and cutout; gesture navigation bar; app switch during combat and return; force-kill and resume from the map; low-memory behavior; every touch target reachable by thumb; text readable at 100% and 130%; scroll lists with drags; rapid tapping on cards and End Turn; Android back gesture on a modal; Reduce Motion and Haptics settings; portrait lock; frame rate on a mid-range device with the debug monitors; battery behavior over a ten-minute run.

### 19.7 Reporting (TESTREP-01)

docs/TEST\_REPORT.md is a table: test id, command, result, date, evidence tag. A failing test is recorded as failing with its cause. tools/run\_all\_checks.sh (or an equivalent script) runs import, content build, content validation, tests, and the simulation in order and stops at the first failure.

---

## 20. Milestones and Definition of Done

Do not start a milestone until the previous one meets its exit criteria with RAN evidence. Do not expand scope (§3.4) before M5 passes. Stage letters from the original brief map as: A = M0, B = M1, C = M2, D = M3, E = M4 and M5.

| Milestone | Scope | Exit criteria |
| --- | --- | --- |
| M0 Foundation | Audit (docs/AUDIT.md); project settings; folders; four autoloads with real roles; GameConfig; data classes; content build and ContentValidator; test runner; slop scan | Project opens in 4.7.2 with zero warnings; tests run; Content validates; PROGRESS.md and DECISIONS.md exist |
| M1 First loop | Judgment; Karma; traits; starter deck; a simplified map of three nodes; combat with one enemy; one reward; death; settlement; Hub; profile save | A full life plays start to finish; Soul Fragments persist across a process restart (RAN) |
| M2 Combat complete | All 24 cards, 10 statuses, 6 enemies, boss, intents, hostility, reward weights | Combat tests and simulation targets pass; boss defeatable and loseable |
| M3 World | Real map generator, six events, rest, both merchants, factions, four unlocks, run save and resume | Map, event, economy and meta tests pass; each unlock verified in game |
| M4 Polish | Layout audit, settings, accessibility, juice, save recovery UX, art pass | Audit passes at all viewports and 130% text; no slop hits; frame budget measured |
| M5 Verification | Full suite, device checklist, final report | The “Required end-to-end playthrough” below passes on a device or is documented honestly as manual |

**Required end-to-end playthrough:** launch; start a new life; Heaven’s Judgment; Karma classification and Trait Points; legal trait selection; map; a route; an ordinary combat; a reward; a second node; progress toward the boss; the boss fight or a death; the correct Soul Fragment reward; the Hub; an affordable purchase; close and reopen the game; permanent progress intact; a new life with the unlocked content available.

**Definition of Done.** Every item below holds and is evidenced in docs/TEST\_REPORT.md:

- The project opens and runs in Godot 4.7.2 with no parse errors and zero first-party warnings.
- Every item in §3.4 exists with exactly the locked counts.
- Judgment, Karma, traits, map, combat, rewards, boss, death, Hub and unlocks work end to end, and all four unlocks change the game.
- Persistence survives a real process restart; corrupt, missing and future saves recover as §16 specifies.
- The interface passes §17 on every test viewport.
- The slop scan and the Slop Audit pass.
- There are no fake implementations, no TODOs, no dead code.
- The final report states what works, what was tested, what was not, and what remains.

### 20.1 Risk register

| Risk | Mitigation |
| --- | --- |
| Godot cannot run in the agent’s environment | Evidence tags (§2.3); manual procedures; the user runs the test command |
| Hand-written .tres errors | Generated content (§6.5) and ContentValidator |
| Scope creep | Scope lock (§3.4), M-gates, non-goals (§3.5) |
| Rules and text drift apart | Generated text (§6.3) and tests |
| Save corruption | Atomic writes, backups, fixtures (§16) |
| Tiny touch targets and clipped text | Size floors, layout audit, pseudolocalization |
| Low-end device performance | Budgets (§4.7), baked art, no per-frame work |
| Context loss between sessions | Session protocol and progress files (§2.6) |
| Balance outliers | Simulation targets (§11.4), tunables only in config and content |
| Font or audio licensing | Only licensed files with license text and manifest entries |
| iOS export needs macOS and signing | Document the export steps; do not claim an iOS build was produced unless it was |

---

## 21. Scalability Roadmap

The slice is small on purpose. The foundations below let the game grow without rewrites. Nothing in §21.3 is built before M5 passes.

### 21.1 What scales by design

| Growth | How it scales |
| --- | --- |
| New cards, enemies, events, traits, scenarios, unlocks | Add a .tres file; ContentValidator and tests catch mistakes; no code change unless a new effect kind is needed |
| New effect kinds | Extension procedure §21.2 |
| New factions | Faction enum, pool weights (§7.4) and hostility rules (§14.4) |
| New regions | Lift the slice constants in GameConfig into a RegionData resource that parameterizes floors, pools and boss |
| Multi-enemy combat | CombatState already holds an array of enemies; targeting rules are the new design work |
| Save growth | Versioned schema and migrations with fixtures (§16) |
| Localization | tr() everywhere and placeholder-based sentences (§17.6) |
| Narrative depth | Hub unlocks inject flags; content checks flags; flags are registered in KNOWN\_FLAGS |
| Performance headroom | Baked art, atlased icons, pooled views, no per-frame work (§4.7) |

### 21.2 Extension procedure for a new effect kind (EXT-01)

1. Add the enum member.
2. Implement it in the single effect resolver.
3. Add its text template to the text builder.
4. Add tests for resolution, text and serialization.
5. Use it in at least two cards or intents. A kind with fewer than two users is speculation and is rejected.
6. Update the tables in §6.2 and §9 of this blueprint and bump its version.

### 21.3 Post-slice roadmap (priority order; not part of Milestones 0–5)

1. Poisoned Assassin and a wider injury system (the deferred enemy from §1).
2. A second region through RegionData.
3. Relics: run-wide passive modifiers expressed as data like traits.
4. Consumables: a small pouch of single-use items.
5. More Judgment scenarios (target 20) and more flags.
6. **The Ninefold Ledger.** The title promises nine. In the Hub, nine named past lives, each remembering a class of choice (mercy, obedience, defiance, greed and so on) and each granting a permanent flag when its condition is first met. This is the structural payoff of the reincarnation theme.
7. More traits (target 24), including the second Cynic-route trait.
8. Multi-enemy encounters.
9. A daily seed challenge, offline, derived from the date (the deterministic RNG already supports it).
10. Cloud save or leaderboards are out of scope. Pursuing them would require a new security review and a revision of §3.5 and §4.8.

### 21.4 Debt guard and versioning

Every addition ships with data, logic, UI, a test, and a blueprint update. Any deviation from this blueprint gets a DECISIONS.md entry. No new autoload without a DECISIONS entry that cites shared, long-lived state. Scripts stay at 400 lines or fewer. When a locked value changes, edit this blueprint first, bump the version number at the top, and add a line to the change log in docs/DECISIONS.md.

---

## Appendix A. Prompts to Give the Coding Agent

**A.1 Kickoff (first message of the project)**

You are the coding agent for the Godot 4.7.2 project specified in docs/BLUEPRINT.md. Read it completely before acting. Follow §2 (Agent Contract) and §5 (Anti-Slop Charter) throughout. First, perform the Phase Zero audit (§2.4) and write docs/AUDIT.md. Second, create docs/PROGRESS.md, DECISIONS.md, KNOWN\_ISSUES.md, ASSET\_MANIFEST.md and TEST\_REPORT.md. Third, execute Milestone M0, then M1, and at each exit criterion report in the §2.7 format with evidence tags. Make decisions yourself and ask only for the §2.5 blockers. Do not exceed the scope in §3.4. Do not claim anything you did not run.

**A.2 Resume (start of every later session)**

Read docs/BLUEPRINT.md, then docs/PROGRESS.md, docs/DECISIONS.md and docs/KNOWN\_ISSUES.md in that order. Continue from the next concrete step recorded in PROGRESS.md. Do not redo completed work unless a test now fails. End the session by updating PROGRESS.md with evidence tags.

**A.3 Slop audit**

Run the §5.8 Slop Audit on the repository as it stands and run the slop scan test. For every failed question give the file path and a fix, apply the fixes, re-run, and report with evidence tags.

**A.4 Balance pass**

Run the combat simulation, compare each matchup with the §11.4 targets, change tunable values only (never locked values), re-run, and record every change and its before-and-after results in DECISIONS.md.

---

## Appendix B. Glossary

| Term | Meaning in this project |
| --- | --- |
| Alignment class | Orthodox, Neutral or Demonic, derived from the Karma band (§1 row 1) |
| Band | One of Righteous, Positive, Neutral, Tainted, Asura (§7.4) |
| Profile flag | A permanent string in Profile.unlocked\_flags, granted by Hub unlocks |
| Run flag | A string in RunState.flags that lasts one life; set by Judgment (§7.6) or events (§13.2) |
| Judgment flag | A run flag created at the verdict, such as cynic\_route |
| Floor | One row of the map; counted when its node is cleared |
| Intent | The enemy action shown before the player commits their turn |
| Telegraph | An intent whose purpose is to announce the next one (Verdict Charge) |
| Form | Keyword: bonus if the previous card this turn was an Attack |
| Blood Price | Keyword: pay HP instead of Energy |
| Severance | Keyword: the target’s next attack deals less damage |
| Internalize | Keyword: unspent Energy becomes Block |
| Evade | Status: negates incoming hits |
| Unshakable Stance | Status: lets Block carry across turns |
| Qi | Combat resource and the setting’s internal energy |
| Meridians | The channels Qi flows through; used by Qi Disruption, Severance, Bleeding and traits |
| Dantian | The energy reservoir; used by Wounded Dantian |
| Manual | A martial text; in game, a Treasure reward or an Archive card |
| Soul Fragment | The permanent meta-currency |
| Seed code | The run seed written as 8 hex digits |
| CardInstance | A run-time card: immutable CardData plus is\_upgraded and an instance id |
| Slop | Output that looks finished but is generic, unverified, redundant or fake (§5) |

---

## Appendix C. GameConfig Reference (initial values)

Every value lives in scripts/config/game\_config.gd. Tunable unless stated.

| Constant | Default | Section |
| --- | --- | --- |
| PLAYER\_START\_MAX\_HP | 80 | §8.4 |
| PLAYER\_START\_GOLD | 100 | §8.4 |
| MIN\_MAX\_HP | 30 | §8.2 |
| COMBAT\_BASE\_ENERGY | 3 | §9.4 |
| COMBAT\_DRAW\_PER\_TURN | 5 | §9.3 |
| COMBAT\_HAND\_MAX | 10 | §9.8 |
| ENERGY\_CAP | 10 | §9.4 |
| BLOCK\_CAP / BLOCK\_DOUBLE\_MAX\_GAIN | 99 / 30 | §9.8 |
| COMBAT\_MAX\_CARDS\_PER\_TURN / COMBAT\_MAX\_DRAW\_PER\_EFFECT | 40 / 10 | §9.8 |
| WEAK\_PCT / VULNERABLE\_PCT / QI\_DISRUPTION\_PCT | 75 / 150 / 70 | §9.5 |
| STATUS\_CAP\_BLEEDING / STATUS\_CAP\_STANCE | 20 / 30 | §9.5 |
| ENEMY\_MAX\_CONSECUTIVE | 2 | §11.2 |
| REST\_HEAL\_PCT | 30 | §8.4 |
| KARMA\_BANDS | Table in §7.4 | §7.4 |
| KARMA\_DELTA\_MIN / KARMA\_DELTA\_MAX | −12 / 12 (locked) | §7.3 |
| JUDGMENT\_STEPS | 5 (locked) | §7.3 |
| TRAIT\_MAX\_SELECTED / TRAIT\_MAX\_NEGATIVE\_POINTS | 6 / 8 | §8.1 |
| MAP\_NODES\_PER\_FLOOR | 2, 2, 2, 2, 1, 1 (locked) | §12.1 |
| MAP\_MIN\_COMBATS\_PER\_PATH / MAP\_GEN\_MAX\_ATTEMPTS | 2 / 50 | §12.1 |
| MAP\_WANDERER\_CHANCE | 0.35 | §12.4 |
| ECON\_PRICE\_COMMON / UNCOMMON / RARE | 50 / 80 / 140 | §13.4 |
| ECON\_WANDERER\_DISCOUNT\_PCT | 10 | §13.4 |
| ECON\_REMOVAL\_BASE / ECON\_REMOVAL\_STEP | 75 / 25 | §13.4 |
| ECON\_SALVE\_PRICE / ECON\_SALVE\_HEAL\_PCT | 45 / 20 | §13.4 |
| REWARD\_CARD\_CHOICES / REWARD\_CHOICES\_OPEN\_ROAD | 3 / 4 | §13.1 |
| REWARD\_POULTICE\_HEAL\_PCT | 12 | §13.1 |
| REWARD\_RARITY\_WEIGHTS\_STANDARD / ELITE | 60-33-7 / 35-45-20 | §10.6 |
| SOUL\_REGULAR / SOUL\_ELITE / SOUL\_BOSS / SOUL\_PER\_FLOOR | 5 / 20 / 100 / 10 | §15.2 |
| SOUL\_RUN\_CAP | 1000 | §15.2 |
| SAVE\_SCHEMA\_VERSION | 1 (locked per release) | §16 |
| SAVE\_MAX\_BYTES / SAVE\_CORRUPT\_KEEP | 1,048,576 / 3 | §16 |
| CONTENT\_VERSION | 1 (bump when content breaks saves) | §16.5 |
| DECK\_MAX / FLAGS\_MAX | 100 / 256 | §4.8 |
| UI\_MIN\_TOUCH / UI\_GAP\_MIN | 132 / 16 | §17.2 |
| UI\_FADE\_MS | 180 | §17.4 |
| RNG\_SALT\_JUDGMENT, MAP, COMBAT, REWARD, EVENT, SHOP | Six distinct fixed integers (locked once chosen) | §4.5 |

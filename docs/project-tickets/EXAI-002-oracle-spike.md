# EXAI-002 — Headless build import and passive-swap proof

Status: Complete — restricted real-build boss mutation reproduced in fresh workers
Depends on: EXAI-001

## Scope

Decode PoB2 share codes in Python, load XML through upstream `HeadlessWrapper.lua`, read calculated offensive/defensive metrics, apply a legal one-point normal-passive swap through upstream methods, recalculate, and verify unchanged point budgets in fresh workers. Keep encounter settings and objective metadata explicit.

## Acceptance evidence

- [x] Bounded URL-safe Base64 plus zlib/gzip decoding, PoB2 root validation, malformed-input and XML-entity rejection.
- [x] Project-owned diagnostic exported from the pinned PoB2 runtime, with source/hash/provenance recorded.
- [x] Imported and standardized-scenario metrics read programmatically, including DPS, life, energy shield, resistances, EHP, and damage-type max-hit values.
- [x] Normal passive leaf swap through `DeallocNode`/`AllocNode`, complete six-field budget preservation, and connected allocations.
- [x] Import verifies exact allocated node IDs to detect silently dropped allocations.
- [x] CPU startup/load/recalculation timings and end-to-end wall time returned.
- [x] Complete fresh-worker integration suite passes after final review.
- [x] Permissioned real build imported with its active allocation preserved and baseline metrics extracted.
- [x] Audited real-build passive mutation and before/after results validated under the restricted conservative policy.
- [x] Standardized encounter configuration and explicit conditional-override policy recorded for that real build; measured sustained uptime is not claimed.

## Deliberate limits

The generated fixture is a level-90 Sorceress with one paid passive, one level-1 Spark gem, and no equipment. It proves actual PoB import and recalculation, but is not an endgame build or training data. Do not claim the real-build criterion is satisfied by this fixture.

The original diagnostic validation accepts a single Spark gem, one current-tree specification, and no explicit conditional-config overrides, custom modifier blocks, jewel sockets, mastery selections, or weapon-set allocations. A separate restricted Whirling Assault benchmark now admits the reviewed skill family and ordinary stat jewels with explicit configuration normalization. This does not establish general build support. This adapter is a one-shot experiment; the long-lived isolated worker contract belongs to EXAI-003.

The boss scenario overrides boss category, enemy level, and incoming damage-type selection; remaining calculation defaults belong to the pinned engine. It preserves quest rewards and permanent character state rather than clearing all configuration indiscriminately. This is a restricted diagnostic scenario, not a completed general-purpose assumption auditor. The complete versioned objective/constraint and audit policy belongs to EXAI-004.

No optimization or improved-build claim is made: the selected swap deliberately trades damage for energy shield to prove both sides of the calculation boundary.

## Next required input

A build export and explicit redistribution permission have now been provided. The anonymized contribution is `tests/fixtures/gemling-spark-contributed.pobcode`, with provenance alongside it. Its custom modifiers and jewel interactions exceed the agreed audited action space. Complete the real-build mutation criterion using an eligible contributed build or an explicitly agreed, documented derived fixture; do not silently remove mechanics or relabel imported assumptions as an audited benchmark.

Update: the subsequent user-approved Whirling Assault contribution supplies the real-build proof below. No further export is required for this ticket.

## Contributed-build findings

The supplied export is a level-90 Mercenary / Gemling Legionnaire with Spark selected in skill set 8, active tree specification 8, and configuration set 12. It contains progression variants, eight jewel socket records, and an active custom `150% increased cost efficiency` modifier. Explicit active assumptions include Power Charges, Arcane Surge, recently crit, and recently triggered a skill. These are audit requirements, not accusations that the configuration is false.

Read-only `inspect_import` preserves imported settings, rejects version conversions and dropped/added allocation IDs, and always marks results `benchmark_eligible=false` / `as-imported-unverified`. All 132 active allocation IDs survived import. PoB2 returned budget tuple `[121, 8, 0, 6, 0, 0]`; this reports imported counts, not certification that the build is within its level/quest budget.

Configured baseline: CombinedDPS 211277.80852331; Life 1554; EnergyShield 0; TotalEHP 11234.400170098; Fire/Cold/Lightning/Chaos resistances 41/75/67/-21. These are as-imported conditional calculations, not standardized or measured combat performance.

PoB2 reports 11 nodes not directly connected to the class start. This can require special allocation/jewel semantics; the read-only report preserves the IDs and does not classify the build as invalid. Strict passive-mutation evaluation still rejects disconnected allocations.

Import metadata (including lastCharacterHash and lastRealm), notes, display labels/titles, and explicit identity/import URL attributes were removed. Original and anonymized versions were evaluated in separate fresh containers: all reported metrics, allocation IDs, and point counts matched exactly. The original remains under ignored `.local/`; only the anonymized fixture is intended for publication. No Git staging, commits, or pushes were performed.

## Verification record

Full suite with `EXILEAI_POB_INTEGRATION=1`: 24 passed in 43.90 seconds (19 fast checks and 5 container integration cases; reproducibility uses two fresh containers). Ruff lint/format, mypy, and diff whitespace checks pass. Changes remain unstaged, with no commits or pushes performed for this ticket.

Diagnostic oracle results: CombinedDPS 4.6714285714286 → 4.2821428571429; EnergyShield 0 → 10; Life remains 1187; TotalEHP 872.13826500793 → 875.81197294815. Both allocations use budget tuple `[1, 0, 0, 0, 0, 0]`. Full expected metrics are recorded in `tests/fixtures/spark-diagnostic.expected.json` and checked against fresh-worker output with declared tolerances.

An observed diagnostic run reported 2.883 seconds CPU bootstrap, 0.211 seconds CPU load, and 0.076 seconds CPU mutation/recalculation, with 7.07 seconds wall time for the one-shot container request. These are one-run development measurements, not an endgame workload or throughput benchmark; timings remain part of every result.

Review found and fixed legacy Config/Input and string-Placeholder audit bypasses, as well as unrestricted settings under the versioned scenario label. Numerical placeholders are reset to fresh upstream defaults for the scenario. No claim of a complete condition auditor or production evaluator is made.

After adding the permissioned contribution and read-only inspector: the complete suite passes with 27 tests in 48.14 seconds, including six Docker integration cases. The new checks cover anonymization, active-tree selection, retained custom modifiers, baseline metric expectations, and explicit benchmark exclusion.

## Replacement Flameblast export

The user supplied a second export for the swap proof: a level-98 Gemling Legionnaire with Flameblast selected. The anonymized fixture is `gemling-flameblast-contributed.pobcode`, with metadata and item Unique IDs removed. No calculation inputs were deliberately changed. The original attachment remains untouched.

This export has no custom modifiers, but includes two nonempty 24-point weapon-set branches and Voices granting two free sockets. Read-only inspection preserves all 157 saved allocations and reports the two additional item-granted nodes, 26178 and 62152, explicitly as free/granted. No saved node was dropped. The returned point tuple is `[146, 8, 0, 9, 24, 24]`; all nodes are directly connected.

As-imported calculated results: CombinedDPS 15565539.904953; TotalDPS (hit component) 180416.46381579; Life 3257; EnergyShield 0; TotalEHP 113962.62425447. Combined and hit DPS are distinct and must not be conflated with measured sustained combat performance. PoB2 also reports Dexterity 64 versus required 76, a pre-existing deficit that prevents a feasible recommendation under the current requirement rule.

Attempted ordinary swaps were rejected: removing 3652 and adding 9884 produced point counts `[145, 8, 0, 9, 24, 23]`, while removing 26952 and adding 9884 produced `[141, 8, 0, 9, 22, 21]`. Upstream's dependency rebuild altered weapon-set allocations, so neither meets the unchanged-budget contract. These are rejected diagnostic trials, not accepted recommendations or proof of an upstream bug. The temporary fixture-specific mutation bypass and failing request were removed; general mutation eligibility remains strict.

The read-only report now distinguishes saved allocations from explicitly listed runtime additions/removals. This avoids treating legitimate Voices grants as silent data loss while preserving exact checks in the ordinary mutation path. A documented simplified derivative or validated weapon-set-aware action handling is required before this build can complete the real-build mutation criterion. Do not remove its mechanics silently.

Final replacement-fixture verification: 29 tests passed in 57.40 seconds, including seven Docker integration cases. Ruff lint/format, mypy, and diff whitespace checks pass. All changes remain unstaged; no Git add, commit, or push was performed.

## Whirling Assault selection (2026-10-17)

The subsequent level-96 Monk / Martial Artist export imports with all 131 saved allocation IDs preserved, no disconnected nodes, and point tuple `[121, 8, 0, 4, 0, 0]`. Its selected group 9 is disabled Wind Dancer. With explicit user approval, a private anonymized derivative selects enabled group 8, Whirling Assault. Gear, allocations, gem groups, and configuration remain unchanged. The original and derivative are under ignored `.local/`, alongside an explicit audit record; the user attachment is untouched.

The selected derivative returns as-imported CombinedDPS 878963.48805864, TotalDPS 556467.25321782, Life 1, EnergyShield 8657, TotalEHP 61878.307928632, and physical/fire/cold/lightning maximum hits 8658/30921/30921/33300. There are no attribute deficits. These are conditional imported calculations, not certified sustained boss DPS. A reduced inspection request omitted chaos maximum hit explicitly; no acceptance check was weakened.

A private raw-output diagnostic establishes `ChaosInoculation=true` and numeric positive infinity for `ChaosMaximumHitTaken`. The current finite-only collector rejects that output intentionally. The evaluator needs explicit immunity/non-finite metric semantics before supporting this case; do not replace infinity with zero, a large arbitrary number, or unrestricted non-standard JSON Infinity.

The export explicitly enables recent kills, power charges, rage 30, combo 5, resonance 180, shock effect 28, multiple enemy conditions and recent-event flags. Kill-dependent assumptions are not justified by a sustained isolated boss scenario; other uptime and magnitude assumptions require mechanic-specific evidence. None have yet been silently cleared or certified. Quest rewards and permanent state must remain intact during future normalization.

At that checkpoint no real-build passive swap had been accepted. The mutation preflight only supported the single-Spark diagnostic, so supporting this build required a reviewed eligibility extension as well as assumption auditing and immunity-aware output handling. No fixture-specific whitelist or guard bypass was introduced. Baseline fast suite: 22 passed, 7 integration tests skipped; selected-skill inspection and raw immunity probe both ran in fresh network-disabled containers.

## Completed real-build proof under a conservative policy

The later approved implementation adds explicit chaos-immunity output handling, `benchmark_swap` preparation with `conservative-boss-conditions-v1`, and structural admission for the restricted Whirling Assault skill family and plain stat jewels. It preserves the contributed equipment, skill groups/supports, passive attribute choices and jewel sockets. Unknown configuration keys, quest choices and unreviewed jewel effects fail closed. There is no fixture-hash admission bypass. The versioned encounter and diagnostic objective remain separate request metadata.

The anonymized public fixture retains its imported assumptions; normalization happens in the adapter and reports every setting change. Unverified overrides are disabled conservatively; quest rewards are retained, imported placeholders are reset, enemy isolation is retained for the no-adds encounter, and distance is fixed to two metres. Enabled skills/supports and intrinsic engine effects are retained. This defines a reproducible static benchmark, not a guarantee of buff uptime, sustain or measured encounter DPS. It does not assert the original assumptions were dishonest or necessarily impossible.

The legal normal-passive swap removes 52399 (Quarterstaff Critical Damage) and allocates 9050 (Attack Speed). All six budget fields remain `[121, 8, 0, 4, 0, 0]`; all other allocation IDs/modes, connectivity and attribute requirements are preserved. Exported fixed inputs are checked independently of cached calculation output records. Before/after CombinedDPS is 242864.38829736 / 235633.49232952; TotalDPS is 151359.02365497 / 148030.88532174. Life stays 1, EnergyShield 8657, TotalEHP 49308.744871913, and all recorded finite defensive metrics are unchanged. This is a diagnostic, not an improved-build recommendation.

Chaos maximum hit is explicitly null with `immune` / `ChaosInoculation` metadata. Deltas involving immunity are null with before/after states; unrelated missing or non-finite metrics still fail. `monk-boss-spike-request.json`, `monk-boss-spike.expected.json` and the fixture provenance make the proof reproducible in fresh workers. Observed one-run timings: bootstrap 2.523 seconds CPU, original import 0.484 seconds CPU, mutation/recalculation 0.121 seconds CPU, complete request 7.63 seconds wall time. These are diagnostic measurements, not throughput benchmarks.

The new integration test evaluates the swap in two independent containers and checks expected metrics with relative tolerance `1e-9` / absolute tolerance `1e-8`. Unit tests cover config audit output, malformed/unknown settings, unreviewed mechanics, fixture provenance and fixed-input mutation guards. Final full-suite verification and review are recorded below before ticket closure.

Final verification: **50 passed in 79.18 seconds**, with `EXILEAI_POB_INTEGRATION=1` (41 fast cases and 9 container integration cases). Ruff lint and format checks, strict mypy, and diff whitespace checks pass. The empty metric-state case is a JSON object, not an array. Effective runtime configuration is returned as `resolved_config_inputs`; it includes upstream defaults and is not a list of user-enabled buffs. The original/source configuration, policy changes, encounter and objective remain separately identifiable.

Current-file review checked the approved ticket against structural admission, unchanged fixed inputs, full budget and allocation invariants, immunity handling, audit labeling, and test evidence. The commit-range review skill cannot cover these uncommitted/untracked additions as a committed diff; no staging or commits were created to accommodate it. No blocking finding remains from the direct current-file review. The next ticket is EXAI-003; general assumption validation, defensive-floor/objective comparison and additional profiles remain in their assigned later tickets.

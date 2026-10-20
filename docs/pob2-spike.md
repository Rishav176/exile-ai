# Headless PoB2 integration experiment

## Run

With Docker Desktop running Linux containers and the setup environment installed:

```powershell
.\.tools\Scripts\uv.exe run --locked python scripts/pob_spike.py --code tests/fixtures/spark-diagnostic.pobcode --request tests/fixtures/spark-spike-request.json
$env:EXILEAI_POB_INTEGRATION = '1'
.\.tools\Scripts\uv.exe run --locked pytest tests/integration/test_passive_spike.py
Remove-Item Env:EXILEAI_POB_INTEGRATION
```

The first command emits structured results to stdout and upstream diagnostics to stderr. It reports imported, scenario-before, and scenario-after metrics, exact allocation IDs and budget tuples, deltas, CPU timings, wall time, runtime pin, scenario, and objective metadata. XML hashes identify inputs/outputs without printing build contents. The Python experiment helper retains original and evaluated XML in memory for integration checks; the CLI currently reports hashes rather than exporting a recommended build.

Containers receive requests on stdin, mount the repository read-only, disable networking, and are removed on exit. Source revision and a clean upstream checkout are verified before every experiment. Docker CLI failures and Lua errors are diagnostic failures, never fabricated metric results. A 180-second timeout bounds each experiment.

## Fixture provenance

`spark-diagnostic.pobcode` was exported by the pinned PoB2 engine from the project-authored `create_fixture` recipe in `scripts/pob_spike.lua`. Its provenance manifest records the decoded XML hash, class, skill, level, point tuple, engine and tree versions. It contains no third-party character/account data.

This is a synthetic integration diagnostic, not a real player build. The one-point tree and unequipped character do not represent endgame performance or support any optimizer quality claims. The separate Whirling Assault proof below exercises a contributed endgame build.

## Permissioned real-build inspection

The contributor explicitly authorized an anonymized fixture, now stored as `tests/fixtures/gemling-spark-contributed.pobcode`. It preserves skills, gear, passives, and calculation settings. Metadata removal was verified by evaluating the original and anonymized exports in separate containers and comparing exact metrics, allocations, and budgets.

```powershell
.\.tools\Scripts\uv.exe run --locked python scripts/pob_spike.py --code tests/fixtures/gemling-spark-contributed.pobcode --request tests/fixtures/gemling-import-request.json
```

This operation is read-only: no scenario normalization or passive mutation occurs. Results are labeled `as-imported-unverified` and never qualify as audited benchmark samples. It supports selecting the active tree from multiple specifications and reports exact saved-versus-runtime allocation differences, including free/granted nodes, together with non-direct connections. It does not silently certify added/missing nodes as valid. Mutation retains the stricter exact-allocation validation path.

The active contribution uses custom cost-efficiency modifiers and explicit buff/charge assumptions, and has jewel interactions outside the initial mutation scope. It currently proves real-build import and baseline extraction only. See EXAI-002 for measured baseline values and remaining acceptance criteria. `config_inputs` is runtime-resolved configuration and includes upstream defaults; do not mislabel every entry as a user-enabled buff.

The user also supplied `gemling-flameblast-contributed.pobcode` as a replacement candidate. Inspect it with the same request file and a different `--code` path. It has no custom modifiers, but has two weapon-set allocations and Voices-granted sockets. Its imported requirements include a 12-Dexterity deficit, and tested ordinary swaps altered weapon-set budgets. It is retained as a read-only regression case; EXAI-002 documents those rejected trials. No successful mutation of that Flameblast export is claimed.

## Real-build conservative boss proof

```powershell
.\.tools\Scripts\uv.exe run --locked python scripts/pob_spike.py --code tests/fixtures/monk-whirling-assault-contributed.pobcode --request tests/fixtures/monk-boss-spike-request.json
```

The permissioned level-96 Monk fixture selects Whirling Assault with user approval, rather than the original disabled Wind Dancer selection. Its stored configuration remains as imported. The `benchmark_swap` operation performs an explicit, reported normalization before changing a passive; it never treats the imported result as an audited sample. Provenance and input/expected-result files live next to the fixture.

`conservative-boss-conditions-v1` is separate from the three-field `solo-sustained-pinnacle-v1` encounter preset and the diagnostic objective. It preserves the reviewed quest rewards, resets imported placeholders to fresh pinned-engine defaults, and disables unverified recent-event, kill, charge, rage, combo, resonance, shock and enemy-debuff overrides. The no-adds encounter retains enemy isolation and fixes distance at 20 PoB units (two metres). Every explicit override and placeholder reset is included in `assumption_audit.settings`, with prior values and reasons. This conservative policy can understate credible build effects; it does not establish that the imported assumptions were false.

`resolved_config_inputs` records the effective runtime inputs, including upstream defaults, separately from the exported user overrides and their audit. The source/runtime pin determines remaining engine defaults. Future dataset schemas must retain this context, not just a boss-DPS scalar.

Enabled skills, supports, fixed equipment and intrinsic engine effects remain part of the build. PoB does not simulate player rotations or verify uptime, mana sustain or actual encounter performance here. Treat these as reproducible static calculations under the stated policy, not measured sustained boss DPS. Conditional-uptime validation and optional user-assumed profiles remain EXAI-004 work.

Admission is structural, not a fixture-hash bypass: one current tree, one skill/configuration set, an enabled Whirling Assault main group, the restricted reviewed skill family, known quest/configuration keys, no party/custom modifiers/masteries/weapon-set branches, and plain rare Sapphire jewels with reviewed stat lines. New skill families, jewel effects or configuration fields fail closed pending validation. Other fixed item effects are calculated by PoB, not reimplemented. Only ordinary non-attribute leaf swaps are admitted; all allocation IDs, connectivity, attribute requirements, allocation modes and six budget counts are checked. Exported fixed equipment, skills, configuration, class/ascendancy, jewel sockets and attribute choices must remain unchanged after the swap. Cached exported PlayerStat/MinionStat results are outputs, not frozen inputs.

The test swaps 52399 (Quarterstaff Critical Damage) for 9050 (Attack Speed). CombinedDPS changes from 242864.38829736 to 235633.49232952; Life stays 1, EnergyShield 8657 and TotalEHP 49308.744871913. All recorded finite defensive metrics remain unchanged and the budget stays `[121, 8, 0, 4, 0, 0]`. This deliberately non-improving swap proves recalculation, not optimizer quality. Full expected metrics are in `monk-boss-spike.expected.json` and checked in two fresh workers with relative tolerance `1e-9` / absolute tolerance `1e-8`.

### Immunity metric contract

Finite metrics remain numbers. The specific combination of positive-infinite `ChaosMaximumHitTaken` and PoB's `ChaosInoculation=true` is represented as `metrics.ChaosMaximumHitTaken=null` plus `metric_states.ChaosMaximumHitTaken={"state":"immune","reason":"ChaosInoculation"}`. It is neither zero nor an arbitrary large finite value. Other missing, NaN or infinite outputs still fail explicitly. A delta involving immunity is null with before/after states in `delta_states`; do not subtract, score or rank the null value as a number. JSON serialization disallows non-standard NaN/Infinity literals. Generic immunity and objective/constraint comparison semantics belong to the worker/objective tickets.

## Boundary verified by source

- [Headless bootstrap and XML loading](https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2/blob/bb52d6b368307457eb9c54bb13f1829993d390b1/src/HeadlessWrapper.lua): initializes upstream state and supplies `loadBuildFromXML`.
- [Headless runtime stubs](https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2/blob/bb52d6b368307457eb9c54bb13f1829993d390b1/src/_SimpleGraphic.def.lua): compression is stubbed, so transport decoding stays in Python.
- [Passive operations and budgets](https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2/blob/bb52d6b368307457eb9c54bb13f1829993d390b1/src/Classes/PassiveSpec.lua): use upstream allocation/deallocation methods; `CountAllocNodes()` returns ordinary, primary-ascendancy, secondary-ascendancy, socket, weapon-set-1, and weapon-set-2 counts.
- [Calculation output](https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2/blob/bb52d6b368307457eb9c54bb13f1829993d390b1/src/Classes/CalcsTab.lua): `BuildOutput()` provides the `mainOutput` table.
- [Boss settings](https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2/blob/bb52d6b368307457eb9c54bb13f1829993d390b1/src/Modules/ConfigOptions.lua): the pinnacle preset sets enemy modifiers and level-dependent placeholders. Our diagnostic fixes enemy level to 82 and EHP damage type to Average. Exact defaults are versioned by the engine pin, not assumed to be universal game truths.

The scenario and objective are carried as separate request fields. The experiment computes metrics only; `diagnostic-metrics-v1` explicitly does not rank builds. Future profiles and training samples must preserve this separation.

The restricted versioned preset requires its complete three-field configuration and rejects extra or altered fields. Imported numerical placeholders are reset to fresh upstream defaults before applying it. Preflight inspects current and legacy config inputs and string placeholders, which upstream can interpret as inputs; unverified condition overrides are rejected rather than silently accepted.

## Interpretation and known limits

Swap node 4739 (Spell Damage) for node 44871 (Energy Shield), retaining the class-start node and one paid point. Expected behavior is lower Spark DPS and higher energy shield. Reproducibility compares fresh worker metrics with relative tolerance `1e-9` and absolute tolerance `1e-8`; timings and XML serialization order are not assumed deterministic.

Verified diagnostic output: CombinedDPS 4.67143 → 4.28214, energy shield 0 → 10, life unchanged at 1187, and EHP 872.138 → 875.812. These values describe the unequipped synthetic fixture, not a practical endgame recommendation. Full pinned expectations are in `tests/fixtures/spark-diagnostic.expected.json`.

The 14 startup missing-node diagnostics originate while upstream constructs connector polygons in `PassiveTree.lua`, where references absent from `nodeMap` are skipped. That identifies their immediate source, but does not prove all real builds are unaffected. The spike requires imported allocations to match exactly and verifies connectivity before/after each swap; real-build impact still needs checking.

Imported manual condition overrides fail the original synthetic mutation preflight with an audit-needed message. The separate restricted boss operation explicitly normalizes its known inputs and reports changes. Upstream runtime defaults must not all be labeled user-enabled buffs: they include quest rewards, resistance penalties, and unrelated skill options. General auditing, reliable sustained uptime, and user-override labeling remain later work.

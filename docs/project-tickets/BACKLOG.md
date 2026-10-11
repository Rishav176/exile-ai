# ExileAI project tickets

Work through these tickets in order. Complete the acceptance criteria, record verification evidence, and update status before starting the next ticket. These are local tickets, ready to copy into GitHub Issues when the repository remote is confirmed.

EXAI-001 is **Complete**; subsequent tickets remain **Open**. Existing scaffolding must be inspected and reused before implementation. The prior PoB2 research is an input to verification, not proof that the real-build oracle spike already works.

The accepted [optimization contract](../optimization-contract.md) and [discovery decisions](../project-discovery.md) refine the tickets below. In particular, encounter profiles and optimization modes are separate; scenarios/objectives/constraints are explicit inputs; defensive minima replace mandatory preservation of every defensive statistic; and V1 implements the standardized boss benchmark with passive-only changes. Currency-aware item/gem optimization is post-V1.

| ID | Ticket | Depends on |
| --- | --- | --- |
| EXAI-001 | Initialize repository and required software | None |
| EXAI-002 | Prove PoB2 headless evaluation and a budget-preserving passive swap | 001 |
| EXAI-003 | Build an isolated, versioned PoB evaluation worker | 002 |
| EXAI-004 | Define legal passive actions and objective profiles | 003 |
| EXAI-005 | Implement random and greedy search baselines | 004 |
| EXAI-006 | Implement beam and genetic search baselines | 005 |
| EXAI-007 | Generate versioned oracle datasets | 004, 006 |
| EXAI-008 | Train and evaluate a passive-tree GNN action ranker | 007 |
| EXAI-009 | Implement and benchmark GNN-guided search | 008 |
| EXAI-010 | Expose evaluation and optimization through FastAPI | 006, 009 |
| EXAI-011 | Build the Next.js build-import and optimization interface | 010 |
| EXAI-012 | Package reproducibility, deployment, and resume evidence | 011 |

## EXAI-001 — Initialize repository and required software

Status: Complete. Detailed scope and verification: [EXAI-001-initialization.md](EXAI-001-initialization.md).

## EXAI-002 — Prove PoB2 headless evaluation and a budget-preserving passive swap

Status: Open. Depends on: EXAI-001.

Inspect the pinned upstream source and runtime, then implement the smallest repeatable evaluation proof. Decode a permissioned real PoB2 share code in Python, validate the XML, load it headlessly, extract offense and defense, apply a legal one-point swap through PoB2's passive methods, and recalculate. Keep calculations inside PoB2.

Acceptance criteria:
- A fixture records its origin, permission to redistribute, main skill, configuration, game/tree version, and engine revision.
- An automated integration check emits before/after DPS, life, energy shield, applicable EHP/max-hit metrics, action IDs, and passive budgets.
- All applicable point budgets are unchanged; the resulting allocation is connected and legal.
- A fresh worker reproduces results within documented numerical tolerance.
- Unsupported versions, malformed input, missing metrics, and invalid actions fail explicitly.
- Cold startup, build loading, and recalculation timings are recorded.

## EXAI-003 — Build an isolated, versioned PoB evaluation worker

Status: Open. Depends on: EXAI-002.

Wrap the proven Lua adapter in a single-job-at-a-time worker process with a versioned request/response contract. Use canonical build reloads until cheaper rollback is proven equivalent.

Acceptance criteria:
- Requests and results contain engine revision, schema version, build/configuration identity, metrics, and complete budget information.
- Process timeouts, crashes, and invalid requests produce structured errors and worker replacement.
- Repeated and interleaved build evaluations do not contaminate one another.
- Input size limits and bounded decompression prevent uncontrolled resource consumption.
- Worker diagnostics are separate from machine-readable output; builds are not logged by default.

## EXAI-004 — Define legal passive actions and objective profiles

Status: Open. Depends on: EXAI-003.

Implement candidate generation and validation for ordinary passive-tree reallocations. Start with simple leaf swaps; explicitly declare unsupported mastery, ascendancy, jewel, attribute-choice, and weapon-set cases. Define DPS, survivability, and balanced objectives under fixed scenario configuration.

Acceptance criteria:
- Every accepted action preserves connectivity and the relevant budgets and requirements.
- Invalid candidates are rejected before scoring, with PoB2 verifying final state.
- Objective formulas, metric selection, normalization, defense constraints, and missing-value behavior are versioned and documented.
- Search results include original allocation, proposed allocation, deltas, and constraint checks.

## EXAI-005 — Implement random and greedy search baselines

Status: Open. Depends on: EXAI-004.

Implement seeded random search and greedy improvement against the same oracle and action contract.

Acceptance criteria:
- Both algorithms support all objective profiles, bounded evaluation counts, and reproducible seeds.
- The original build is retained when no valid improvement is found.
- Oracle caching includes engine revision and complete calculation context.
- Benchmarks report score improvement, oracle calls, runtime, and failure rate on fixed fixtures.

## EXAI-006 — Implement beam and genetic search baselines

Status: Open. Depends on: EXAI-005.

Add beam search and a genetic baseline using the same validity and scoring rules.

Acceptance criteria:
- Beam width, generations/population, seeds, and stopping rules are configurable and recorded.
- Mutation/crossover produce valid candidates or reject them explicitly; no silent budget drift occurs.
- All four baselines are compared under matched oracle-call budgets and matched runtime budgets.
- Results include repeat-seed variation and per-build performance, not only an aggregate best case.

## EXAI-007 — Generate versioned oracle datasets

Status: Open. Depends on: EXAI-004 and EXAI-006.

Generate graph/build/action/outcome examples using PoB2 labels, including rejected actions and valid actions that worsen a build.

Acceptance criteria:
- Dataset manifests record source provenance, configuration, tree version, engine revision, generator version, seeds, and hashes.
- Examples retain before/after metrics and constraints rather than only a single score.
- Splits are grouped by source build and related variants to prevent train/test leakage.
- Generation can resume and deduplicate examples; a small reproducible dataset validates the pipeline.
- Schema and quality checks catch missing/nonfinite metrics and illegal allocations.

## EXAI-008 — Train and evaluate a passive-tree GNN action ranker

Status: Open. Depends on: EXAI-007.

Implement graph features and a PyTorch/PyTorch Geometric model that ranks candidate changes conditioned on the build and objective.

Acceptance criteria:
- Features include tree connectivity and allocation plus relevant build/action context without exposing outcome labels.
- Training, checkpoints, configurations, seeds, and held-out splits are reproducible.
- Compare against random ranking and a simple non-GNN learned model.
- Report ranking quality, selected-action regret, constraint validity, and ablations on unseen builds.
- Document limits across classes, archetypes, and oracle/tree versions.

## EXAI-009 — Implement and benchmark GNN-guided search

Status: Open. Depends on: EXAI-008.

Use the GNN to prioritize beam-search candidates, with PoB2 evaluating every reported final result. Add MCTS only after guided beam search is measured and a separate experiment justifies it.

Acceptance criteria:
- Compare guided and unguided search under matched oracle-call and runtime budgets.
- Report improvement, time to improvement, model overhead, and robustness on held-out builds.
- A missing or incompatible model falls back to a baseline.
- Final recommendations include verified oracle deltas and exact budget checks.

## EXAI-010 — Expose evaluation and optimization through FastAPI

Status: Open. Depends on: EXAI-006 and EXAI-009.

Provide build validation, asynchronous optimization jobs, job progress/cancellation, results, and PoB-compatible export.

Acceptance criteria:
- Typed, versioned endpoints use isolated workers with queue/concurrency limits and timeouts.
- Job results record algorithm, objective, engine/model version, constraints, and measured deltas.
- API integration checks cover import, submit, progress, cancel, failures, and export/reimport.
- Resource limits and operational diagnostics are documented.

## EXAI-011 — Build the Next.js build-import and optimization interface

Status: Open. Depends on: EXAI-010.

Provide paste/import, configuration review, objective selection, optimization progress, before/after comparison, passive changes, and export.

Acceptance criteria:
- A user completes import → optimize → review → export through the UI.
- Scenario assumptions and tradeoffs are visible alongside offensive/defensive changes.
- Unsupported builds and worker errors produce actionable messages.
- Loading, cancellation, empty-result, and accessibility behavior are verified.

## EXAI-012 — Package reproducibility, deployment, and resume evidence

Status: Open. Depends on: EXAI-011.

Prepare a reproducible demo and engineering/ML report that documents architecture, decisions, datasets, experiments, limitations, and operational behavior.

Acceptance criteria:
- A clean checkout follows documented setup to run a sample end to end.
- CI and deployment configuration pin application, oracle, model, and data versions.
- Benchmarks, ablations, failure analysis, and demo artifacts support any performance claims.
- Distribution preserves upstream and bundled third-party notices.
- Resume bullets describe measured outcomes and the implemented contribution.

## Later scope

Create separate tickets after the passive-tree workflow is validated: skill/support-gem optimization; item optimization and pricing; GGG OAuth/character import; LLM explanations of structured, verified results. Each requires its own integration investigation and acceptance criteria. The LLM does not calculate build quality.

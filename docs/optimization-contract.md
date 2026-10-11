# ExileAI optimization contract

Status: Discovery decisions accepted; consolidated scope awaits user confirmation before implementation. Exact metric formulas and schemas require pinned-engine investigation.

## Independent inputs

An optimization request identifies the baseline build; a versioned encounter configuration; an assumption policy; a versioned objective definition; hard constraints; a legal action space; and a search evaluation/time budget. Search budgets, passive-point budgets, and future currency budgets are distinct quantities.

The evaluator computes structured metrics for the complete candidate build under the supplied scenario. The objective ranks those metrics. Constraint checks decide feasibility. Search proposes candidate combinations. None of these layers hardcodes pinnacle-boss DPS as the universal target.

The initial implementation provides one solo sustained pinnacle-boss benchmark and passive-only actions. Extensibility is achieved through these boundaries; it does not require implementing mapping, pricing, item/gem search, or unused infrastructure in the spike.

## Profiles and modes

Encounter profiles describe Mapping, Bossing, and Balanced play. Optimization modes express DPS, Survivability, and Balanced preferences. A future mapping damage objective should use mapping-relevant damage/coverage proxies and retain a single-target damage floor; selecting DPS must not silently replace mapping objectives with pinnacle single-target DPS.

Mapping will consider supported damage proxies, AoE, mobility, and survivability. Proxy availability must be established against PoB2. Actual clear speed requires observational data or a separately validated predictor. Bossing uses sustained single-target damage and survivability under its encounter. A Balanced encounter profile evaluates both contexts and exposes tradeoffs, rather than inventing an unexplained combined score.

## Assumptions and defense

Preserve original import settings and report imported versus audited results separately. Audited benchmarks admit effects with evidence of a build source and sustained availability. Recheck evidence when allocations change. Future user-assumed uptime is explicitly labeled, recorded, and excluded from audited benchmark comparisons. Do not call uncertain assumptions fraudulent or necessarily inflated.

User-defined defensive minima are hard constraints under a fixed scenario. Suggest audited baseline values as editable defaults. If explicit minima are unmet, search for a feasible allocation; if none is found within budget, report no feasible result found without silently relaxing constraints or claiming global infeasibility. Track other defensive deltas separately. Strict preservation is an optional constraint policy. Missing required metrics or unsupported mechanics must not silently pass feasibility checks. The precise supported metric set and numerical tolerances require pinned-engine investigation.

Survivability mode defaults to an offensive floor equal to audited baseline damage, with an editable tolerance. Balanced mode returns a small set of feasible non-dominated evaluated candidates and explicit metric deltas. Do not claim to have recovered a global Pareto frontier.

## Future currency constraints

V1 preserves the passive-point budget and assumes affordable respecs. Later, item/gem actions include cost data and a complete upgrade plan must cost no more than the user's available currency. Currency conversion, price uncertainty, and acquisition semantics require later decisions before implementation.

The model predicts performance; the optimizer enforces cost and feasibility and searches combinations. PoB2 verifies the entire changed build. Cache keys and training examples include the full candidate context so interacting upgrades are never scored by simply summing isolated gains.

## Dataset and experiment provenance

Examples and experiment results record the encounter configuration, objective definition, assumption policy, constraints, actual metric outcomes, and relevant engine/tree/model/schema versions. Retain full configurations as well as identifiers/hashes. A boss-only training corpus must not be represented as validated mapping optimization.

Begin with reproducible project-owned fixtures and permissioned contributed builds. Record provenance and remove account-identifying information. Review permissions before larger public collection. Group related source builds and their generated variants in the same data split.

## Ticket implications

- EXAI-002: prove the standardized boss benchmark and before/after metrics; preserve imported settings separately.
- EXAI-003: make scenario explicit in the oracle contract; compute metrics independently of ranking objectives.
- EXAI-004: define modular objectives, hard constraints, and assumption eligibility; implement only the initial supported boss scope.
- EXAI-005/006: use objective/constraint/action contracts shared by all search methods; avoid algorithm-specific boss formulas.
- EXAI-007/008/009: carry scenario and objective context through generation, training, and evaluation; preserve leakage-resistant held-out comparisons.
- EXAI-010/011: expose audited versus assumed inputs and configurable constraints with clearly labeled results.
- Post-V1: introduce costed item/gem plans through the existing action and constraint boundaries.

# ExileAI project discovery

Status: Project-level understanding confirmed by user; EXAI-001 implementation authorized. WSL2 + Docker Desktop with Linux containers selected for reproducible evaluation workers.

## Requirements already established by the user

- Working directory: `C:\Coding\ExileAI`.
- Build a resume-grade software/AI project focused on Path of Exile 2.
- Use Path of Building 2 as the deterministic evaluation engine.
- Begin with passive allocation optimization while preserving the passive-point budget.
- Support offensive, defensive, and balanced objectives.
- Prove headless import, metric extraction, passive mutation, and recalculation before substantial implementation.
- Compare non-ML search baselines with a substantive learned approach.
- Keep LLM explanations grounded in structured oracle results.
- Document architecture, experiments, benchmarks, and decisions.
- Create tickets first, then implement them one by one; initialization is the first ticket.

## Round 1: Project boundaries

Accepted decisions:

1. Prioritize a reproducible command-line optimizer and benchmark report proving optimization and measurable ML value; build the web interface afterward.
2. Serve endgame players with existing working PoB2 builds. Hold gear and skills fixed while optimizing passive allocations.
3. Use staged milestones: oracle proof and baseline optimizer first, then ML, then UI. No calendar deadline or weekly effort commitment has been specified.
4. Start locally without paid services. Consider paid compute/hosting only after measuring the need and obtaining a spending decision.

## Round 2: Optimization contract

Accepted decisions:

1. Optimize the imported active tree at its current level, preserving class, ascendancy, and the exact allocated-point budget. Begin with ordinary passive swaps and expand to larger reallocations later.
2. Preserve the imported configuration for player-facing evaluation and report its assumptions. Use a separate fixed scenario for benchmarks. Enable only credible, documented conditions in that benchmark; flag/report additional settings that could inflate results. The actual setting policy remains pending source investigation and user agreement, because community acceptance is not a universal or mechanically sufficient rule.
3. Superseded by Round 4: use configurable defensive minimums and an optional strict preservation mode. All modes preserve equipment and skill requirements. Survivability's offensive floor remains to be specified.
4. Search uses a configurable evaluation budget. Return the best oracle-verified candidate found, plus improvement, evaluation count, and elapsed time; make no global-optimality claim.

## Round 3: Support and evaluation boundaries

Accepted decisions:

1. Initially support ordinary passive trees and direct player-damage builds. Detect and explain unsupported mechanics; defer minions, special jewel interactions, and weapon-set-specific allocations. Exact supported damage mechanics must be verified during the oracle spike.
2. Show imported configured results alongside results under the audited scenario. Optimize under the audited scenario by default and preserve the original configuration for export. This supersedes optimizing directly under all imported assumptions; exported results may differ from audited results and must be labeled separately.
3. Judge ML value on held-out builds against matched oracle-evaluation budgets; include model overhead in runtime reporting. Compare search baselines and a simpler learned model. Report neutral/negative findings honestly. No numerical improvement threshold has been promised before baseline measurement.

## Round 4: Scenario evidence and project workflow

Accepted decisions:

1. Initial standardized benchmark: solo, sustained pinnacle-boss encounter. This is the only encounter implemented in the initial technical milestone.
2. Encounter profiles are Mapping, Bossing, and Balanced. Optimization modes are DPS, Balanced, and Survivability; these are distinct dimensions, not interchangeable names. Encounter configuration and objectives remain modular across evaluation, search, datasets, and ML.
3. Mapping prioritizes appropriate damage/clear-speed proxies, AoE, mobility, and survivability. Single-target DPS is a secondary constraint. PoB-computable proxies must not be presented as measured clear speed; actual clear speed requires additional data or a separate predictive model.
4. Bossing prioritizes sustained single-target damage and survivability in a standardized encounter. Balanced profiles compare mapping/bossing tradeoffs.
5. Audited scenarios require a build source and credible sustained availability for conditional effects; uncertain effects are unverified and excluded. Revalidate eligibility after every passive change. A future user option can explicitly assume buffs/charges are active, with results labeled as conditional and kept distinct from audited benchmark results.
6. Initially exclude builds that depend on custom modifiers from benchmark eligibility, explaining the limitation; reviewed exceptions are deferred.
7. Defensive constraints are user-configurable minimums for life, energy shield, resistances, and relevant max-hit/EHP under a fixed scenario. Armour, evasion, recovery, and other changes are tracked separately. Offer an optional strict defense-preservation mode. Exact default minimums and strict metric set remain to be specified.
8. V1 optimizes passive allocations with exact passive-point preservation and defensive constraints. Assume respec costs are affordable; do not price trade items or gems in V1.
9. Future item/gem upgrade plans must obey a hard currency constraint on the total proposed plan. Learned models predict performance improvements; the optimizer handles feasibility, cost, and combinations. PoB2 evaluates the complete modified build: individual upgrade gains are not additive.
10. Future training examples record the full encounter configuration and optimization objective, with versions and assumption policy. Initial boss-only data provides no evidence of mapping generalization.
11. Keep local Markdown tickets and publish matching GitHub issues once the remote is established. Finish each ticket with verification evidence and a commit, then report completion before starting the next ticket.

Research outcome: PoB2 configuration supports forced combat states, custom modifiers, and party effects; all need audit coverage. No universal authoritative community checklist was identified. Define ExileAI's explicit versioned policy instead. Primary sources: https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2/blob/dev/src/Modules/ConfigOptions.lua and https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2/blob/dev/src/Classes/ConfigTab.lua . Reverify exact fields against the selected pinned revision.

## Round 5: Remaining optimization semantics

Accepted decisions:

1. Suggest audited baseline defensive values as editable default minima. When explicit minima are unmet, search for a feasible allocation. If no feasible result is found within the search budget, report that outcome without relaxing constraints or claiming infeasibility has been proved globally.
2. Survivability mode defaults to the audited baseline's damage as an offensive floor, with a user-editable tolerance. Balanced mode returns a small set of non-dominated feasible options, with metric deltas and explicit tradeoffs rather than one opaque combined score. Non-dominance is relative to evaluated candidates, not a claim of a globally complete Pareto frontier.
3. Start with reproducible project-owned fixtures and permissioned contributed builds. Record provenance, remove account-identifying information, and investigate source permissions before larger public collection. Generated variants of the same source build stay in the same train/validation/test split.

## Discovery completion

All project-level decisions raised in this interview are settled. Exact PoB fields, supported mechanics, enemy parameters, metric formulas, numerical tolerances, and runtime compatibility are factual/technical work assigned to the oracle and objective tickets. Any new product tradeoff uncovered there returns to the grill-with-docs workflow.

Next checkpoint: confirm this consolidated scope, then start EXAI-001 only. Finish its acceptance criteria, verification record, and commit, and report completion before moving to EXAI-002.

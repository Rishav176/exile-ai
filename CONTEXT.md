# ExileAI

ExileAI improves passive allocations for existing Path of Exile 2 builds, with Path of Building 2 providing build calculations.

## Language

**Imported build**:
The player's supplied build, including equipment, skills, passive allocations, and calculation settings.
_Avoid_: Character snapshot, loadout (when referring to the whole imported build)

**Passive allocation**:
The selected passive-tree nodes for a build, including any applicable allocation choices.
_Avoid_: Build (when referring only to selected passives)

**Oracle**:
Path of Building 2's evaluation of a build under its calculation settings.
_Avoid_: AI score, LLM calculation

**Candidate**:
A proposed build state evaluated by the oracle. In V1, only passive allocations change; equipment and skills remain fixed.
_Avoid_: New character, replacement build

**Calculation scenario**:
The enemy conditions and assumed combat states under which the oracle evaluates a build.
_Avoid_: Build quality (when referring to conditional calculation results)

**Benchmark scenario**:
A documented calculation scenario applied consistently to compare optimization methods, with conditional effects admitted only under its stated evidence rules.
_Avoid_: Best-case DPS, community-approved configuration (without a defined policy)

**Flagged assumption**:
A calculation setting whose credibility or sustained availability needs explanation before its results can be interpreted confidently.
_Avoid_: Cheating (a flagged setting alone does not establish intent)

**Encounter profile**:
The intended play context: Mapping, Bossing, or a Balanced comparison of both.
_Avoid_: Optimization mode (when referring to the encounter)

**Optimization mode**:
The preference for DPS, Survivability, or Balanced tradeoffs within the selected encounter profile.
_Avoid_: Encounter profile (when referring to ranking preferences)

**Defensive constraint**:
A required minimum for a specified defensive metric under the selected calculation scenario.
_Avoid_: Defense score (when referring to a feasibility requirement)

**Assumed-uptime scenario**:
A calculation scenario in which the user explicitly treats selected conditional effects as active, without claiming their uptime is verified.
_Avoid_: Audited benchmark

**Clear-speed proxy**:
A measurable build property used as an indicator of mapping performance, rather than an observation of actual content-clearing speed.
_Avoid_: Actual clear speed (for PoB-only metrics)

**Upgrade plan**:
A complete proposed combination of build changes, evaluated together for performance, feasibility, and total cost.
_Avoid_: Sum of individual upgrade gains

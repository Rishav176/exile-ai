# ExileAI

Path of Exile 2 passive-tree optimization using Path of Building 2 as the deterministic oracle. Search and ML operate on explicit encounters, objectives, and constraints. See the [optimization contract](docs/optimization-contract.md).

Completed: **EXAI-002, oracle spike**. The digest-pinned Linux PoB2 runtime decodes/imports builds and recalculates budget-preserving passive swaps for a synthetic Spark diagnostic and a permissioned Whirling Assault build under an explicit conservative boss policy. Immunity is represented explicitly; imported assumptions remain distinct from benchmark settings. Both proofs reproduce in fresh workers. Next: EXAI-003, the isolated versioned evaluation worker. Search and ML are later tickets.

- [Setup and manual prerequisites](docs/setup.md)
- [Project tickets](docs/project-tickets/BACKLOG.md)
- [Accepted discovery decisions](docs/project-discovery.md)
- [Domain glossary](CONTEXT.md)
- [PoB2 import/mutation experiment](docs/pob2-spike.md)

## Layout

- `src/exileai`: Python package
- `scripts`: setup diagnostics and PoB runtime smoke check
- `tests`: Python checks, permissioned fixtures, and opt-in pinned-container oracle integration
- `vendor/PathOfBuilding-PoE2`: pinned upstream submodule with full license notices
- `docs`: discovery, contracts, setup, and tickets

FastAPI, Next.js/TypeScript, and PyTorch/PyTorch Geometric are later milestones. Install their dependencies when their tickets need them.

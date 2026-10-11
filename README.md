# ExileAI

Path of Exile 2 passive-tree optimization using Path of Building 2 as the deterministic oracle. Search and ML operate on explicit encounters, objectives, and constraints. See the [optimization contract](docs/optimization-contract.md).

Current work: **EXAI-001, initialization**. Python tooling and the digest-pinned Linux PoB2 runtime pass local verification. No real-build import, search, or model implementation exists yet; the next ticket proves real-build evaluation and passive mutation.

- [Setup and manual prerequisites](docs/setup.md)
- [Project tickets](docs/project-tickets/BACKLOG.md)
- [Accepted discovery decisions](docs/project-discovery.md)
- [Domain glossary](CONTEXT.md)

## Layout

- `src/exileai`: Python package
- `scripts`: setup diagnostics and PoB runtime smoke check
- `tests`: Python checks (oracle integration comes in EXAI-002)
- `vendor/PathOfBuilding-PoE2`: pinned upstream submodule with full license notices
- `docs`: discovery, contracts, setup, and tickets

FastAPI, Next.js/TypeScript, and PyTorch/PyTorch Geometric are later milestones. Install their dependencies when their tickets need them.

# EXAI-001 — Initialize repository and required technologies/software

Status: Complete
Priority: First
Dependencies: None
Unblocks: EXAI-002

## Outcome

A developer can use `C:\Coding\ExileAI` as the working repository, install the required tools, restore the pinned PoB2 dependency, run Python checks, and start a compatible headless PoB2 runtime from documented commands.

## Scope

1. Inspect the current checkout, Git history/remotes, existing scaffold, instructions, and installed tools. Preserve existing work and reuse relevant files.
2. Initialize or repair repository structure for Python core, PoB workers, tests, fixtures, scripts, architecture notes, experiments, and these tickets. Add future frontend directories when implementation needs them.
3. Establish Python 3.12+ with a project environment, dependency lockfile, pytest, and a formatter/linter. Choose and document one dependency workflow (prefer `uv` when practical).
4. Verify Git and repository provenance. Reuse or register a pinned PoB2 Git submodule, retain its full license notices, and document the upstream revision/update process.
5. Establish the agreed WSL2 + Docker Desktop Linux-container runtime using a verified upstream test container pinned by digest. Verify actual syntax/module compatibility with the selected PoB revision. Return links/instructions for any required manual software installation; do not substitute a native runtime without revisiting the decision.
6. Add setup and environment-check commands that report missing prerequisites clearly. Installation requiring machine changes should be performed with the platform's approval mechanism and documented if a reboot/manual step is needed.
7. Configure fast Python checks in CI and a distinct PoB runtime smoke check, with reproducible dependency restoration.
8. Record the application roadmap: FastAPI for the service, Next.js/TypeScript for the UI, PyTorch/PyTorch Geometric for ML. Install their runtime dependencies in the tickets that first use them; choose PyTorch/CUDA together after the training hardware is known.

## Acceptance criteria

- [x] `C:\Coding\ExileAI` contains a usable Git checkout with documented remote state and no unintended loss of existing files.
- [x] Repository layout and setup instructions match the actual commands and files.
- [x] Python environment installs from a reproducible lock/dependency definition and imports the ExileAI package.
- [x] Fast tests and formatting/lint checks pass locally.
- [x] PoB2 restores at the recorded exact revision, with upstream and third-party license notices intact.
- [x] A smoke command boots the headless PoB2 wrapper successfully using the selected runtime, with no unresolved parser or module errors.
- [x] A fresh setup path and prerequisite check are documented; pending OS installation/reboot requirements are explicit.
- [x] CI definitions cover Python verification and the PoB runtime smoke check.
- [x] Verification evidence records tool versions, oracle revision/runtime identity, commands, and results.

## Out of scope

Loading a real character/build and comparing passive changes belongs to EXAI-002. Search algorithms, training, APIs, and UI implementation belong to subsequent tickets. This ticket is complete only when the PoB runtime smoke check works; installing packages alone is insufficient.

## Completion record

Implementation changes: Initialized local Git repository, Python package and locked uv environment, pytest/Ruff/mypy tooling, environment checker, Python CI, explicit-digest PoB container smoke scripts and manual CI workflow, pinned PoB2 submodule, and setup documentation.

Verification evidence: Git 2.47.0.windows.1; Python 3.12.6; uv 0.13.0; WSL 2.6.3.0 with Ubuntu-24.04 and Linux kernel 6.6.87.2-microsoft-standard-WSL2; Docker Desktop 4.94.0 / engine 29.8.2, linux/amd64. Ruff lint and format checks pass, mypy passes, pytest: 1 passed, environment checker: ready=true. PoB2 source bb52d6b368307457eb9c54bb13f1829993d390b1 and runtime sha256:171dc3da232b8c874882e4ae3b3aa4a6e130a6c9450a31904b312435a6bf5daf are pinned in pob-runtime.json. Two fresh network-disabled container runs produced EXILEAI_POB_SMOKE_OK. Upstream emitted 14 missing-tree-node diagnostics, recorded in docs/setup.md; real-build impact is an EXAI-002 investigation. No remote configured and hosted GitHub CI has not run.

Review: Standards and spec reviews identified timeout cleanup and dirty-source acceptance; both were corrected. Final lint, formatting, type checks, package test, and hardened container smoke check pass. No smoke containers remain. The completion commit contains this ticket and the initialized project.

Remaining blockers: None for local setup. No manual installation remains for local evaluation. EXAI-002 has not started. Codex sandbox setup intermittently fails; approved outside-sandbox commands worked for verification. Publishing GitHub issues/CI awaits establishing the remote.

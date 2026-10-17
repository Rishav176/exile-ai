# Development setup

## Current verified environment

- Workspace: `C:\Coding\ExileAI`.
- Git: 2.47.0.windows.1; repository initialized on `main`, with `origin` configured as `https://github.com/Rishav176/exile-ai.git`.
- Python: 3.12.6, with `.venv` created by uv.
- uv: 0.13.0, installed inside the ignored project-local `.tools` environment.
- Ubuntu-24.04 boots under WSL2, kernel `6.6.87.2-microsoft-standard-WSL2`.
- Docker Desktop: 4.94.0; client/server engine 29.8.2; Linux amd64 backend verified.
- PoB2 source: `bb52d6b368307457eb9c54bb13f1829993d390b1`.

## Docker Desktop prerequisite

Install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/). Choose the WSL2 backend and Linux containers. Start Docker Desktop after installation and finish its initial setup. Restart Windows if the installer requests it.

In Settings, verify **General → Use the WSL 2 based engine**. If you want Docker available inside Ubuntu, enable **Resources → WSL Integration → Ubuntu-24.04**. The Windows CLI can run our checks without launching them from Ubuntu. See [Docker's WSL2 instructions](https://docs.docker.com/desktop/features/wsl/).

Open a new terminal after installation. Verify `docker version` shows both client and server and `docker info --format '{{.OSType}}'` returns `linux`. WSL2 already boots here; no new Ubuntu installation is needed. Run `wsl --version` and update with `wsl --update` if Docker requires a newer WSL version.

## Python setup from a clean checkout

Use PowerShell in the repository:

```powershell
python -m venv .tools
.\.tools\Scripts\python.exe -m pip install uv==0.13.0
.\.tools\Scripts\uv.exe sync --locked
.\.tools\Scripts\uv.exe run --locked ruff check .
.\.tools\Scripts\uv.exe run --locked ruff format --check .
.\.tools\Scripts\uv.exe run --locked mypy
.\.tools\Scripts\uv.exe run --locked pytest
.\.tools\Scripts\uv.exe run --locked python scripts/check_environment.py
```

Python 3.12 is selected deliberately for the initial tooling baseline. Dependencies are recorded in `uv.lock`; commit intentional lockfile changes. The environment checker exits nonzero while Docker is missing, stopped, or running Windows containers.

## PoB2 runtime verification

Restore the pinned source with `git submodule update --init --recursive`.

The tested source revision, Linux platform, and immutable upstream image digest are recorded in `pob-runtime.json`. The smoke runner checks that the source checkout matches this manifest. An explicit `--image` override is available for investigating a runtime update; normal runs use the committed digest.

```powershell
.\.tools\Scripts\uv.exe run --locked python scripts/pob_smoke.py
```

Docker automatically pulls the pinned image if absent. To update the runtime intentionally, pull the upstream test tag, inspect its RepoDigests, test the new digest using `--image`, and commit the verified source/image pair in the manifest. Do not use a mutable tag in normal runs.

The smoke script requires a clean pinned upstream checkout, mounts source read-only, disables container networking, creates a fresh build, and checks that calculations produce an output table. It passed locally with `EXILEAI_POB_SMOKE_OK`. Its uniquely named container is forcibly removed on exit, including timeout/interruption. It does not prove real build import or passive mutation; those belong to EXAI-002. Upstream emitted missing-node diagnostics for 14 tree node IDs during initialization; these did not prevent bootstrap. Investigate their impact on real build allocations in EXAI-002.

If a terminal opened before Docker installation cannot find `docker`, reopen it. For a per-user installation, the CLI may be located at `%LOCALAPPDATA%\Programs\DockerDesktop\resources\bin`; no global PATH change was made by this setup.

## Source and licenses

Keep PoB2 changes outside the submodule. Review source/runtime changes explicitly and update the source gitlink and image digest together with verification evidence. Preserve the complete upstream `LICENSE.md`, including bundled third-party notices.

## Completion gate

Local Python checks and the pinned Linux PoB2 smoke check pass. The GitHub remote is configured, and Python and PoB smoke workflows are configured to run on pushes/pull requests. Hosted CI execution has not been verified; no hosted-CI success is claimed.

The user reviews changes and handles staging, committing, and pushing. The agent leaves changes unstaged unless explicitly instructed otherwise.

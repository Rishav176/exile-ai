"""Run the upstream headless bootstrap in an explicitly digest-pinned image."""

import argparse
import json
import re
import subprocess
from pathlib import Path
from uuid import uuid4


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[1]
    runtime = json.loads((root / "pob-runtime.json").read_text(encoding="utf-8"))
    parser.add_argument(
        "--image", default=runtime["image"], help="PoB image digest override"
    )
    args = parser.parse_args()
    if not re.fullmatch(r"[^\s]+@sha256:[0-9a-f]{64}", args.image):
        parser.error("--image must use an immutable sha256 digest")
    if not (root / "vendor/PathOfBuilding-PoE2/src/HeadlessWrapper.lua").is_file():
        parser.error("Restore the PoB2 submodule first")
    revision = subprocess.run(
        ["git", "-C", str(root / "vendor/PathOfBuilding-PoE2"), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    if revision != runtime["source_revision"]:
        parser.error("PoB2 checkout does not match pob-runtime.json")
    dirty = subprocess.run(
        [
            "git",
            "-C",
            str(root / "vendor/PathOfBuilding-PoE2"),
            "status",
            "--porcelain",
            "--untracked-files=all",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    if dirty:
        parser.error("PoB2 checkout has local changes; restore a clean pinned checkout")
    container_name = f"exileai-smoke-{uuid4().hex}"
    command = [
        "docker",
        "run",
        "--rm",
        "--name",
        container_name,
        "--platform",
        runtime["platform"],
        "--network=none",
        "--mount",
        f"type=bind,source={root},target=/workspace,readonly",
        "--workdir",
        "/workspace/vendor/PathOfBuilding-PoE2/src",
        "--env",
        "HOME=/tmp",
        "--env",
        "LUA_PATH=../runtime/lua/?.lua;../runtime/lua/?/init.lua;;",
        "--env",
        "CI=true",
        args.image,
        "luajit",
        "/workspace/scripts/pob_smoke.lua",
    ]
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=180, check=False
        )
    except FileNotFoundError:
        parser.exit(1, "Docker CLI is missing; see docs/setup.md\n")
    except subprocess.TimeoutExpired:
        parser.exit(1, "PoB2 smoke check timed out after 180 seconds\n")
    finally:
        # Docker daemon containers can outlive a killed/interrupted CLI client.
        try:
            subprocess.run(
                ["docker", "rm", "--force", container_name],
                capture_output=True,
                timeout=15,
                check=False,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print(f"Could not confirm cleanup of container {container_name}")
    print(result.stdout, end="")
    print(result.stderr, end="")
    return (
        0 if result.returncode == 0 and "EXILEAI_POB_SMOKE_OK" in result.stdout else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())

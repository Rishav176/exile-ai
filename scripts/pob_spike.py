"""Run the EXAI-002 one-shot PoB experiment; emit a JSON result on stdout."""

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from uuid import uuid4

from exileai.pob.benchmark import prepare_boss_benchmark, validate_fixed_inputs
from exileai.pob.codec import decode_build_code, encode_build_xml
from exileai.pob.validation import (
    active_import_nodes,
    validate_spike_scenario,
    validate_spike_xml,
)


def run_experiment(request: dict[str, Any]) -> dict[str, Any]:
    request = dict(request)
    if request.get("operation") == "inspect_import":
        request["expected_nodes"] = active_import_nodes(request["xml"])
    elif request.get("operation") == "benchmark_swap":
        validate_spike_scenario(request.get("scenario"))
        request["benchmark_xml"], request["assumption_audit"] = prepare_boss_benchmark(
            request["xml"]
        )
        request["expected_nodes"] = active_import_nodes(request["xml"])
    elif request.get("operation") != "create_fixture":
        validate_spike_scenario(request.get("scenario"))
        request["expected_nodes"] = validate_spike_xml(request["xml"])
    root = Path(__file__).resolve().parents[1]
    runtime = json.loads((root / "pob-runtime.json").read_text())
    vendor = root / "vendor/PathOfBuilding-PoE2"
    revision = subprocess.check_output(
        ["git", "-C", str(vendor), "rev-parse", "HEAD"], text=True
    ).strip()
    dirty = subprocess.check_output(
        ["git", "-C", str(vendor), "status", "--porcelain", "--untracked-files=all"],
        text=True,
    ).strip()
    if revision != runtime["source_revision"] or dirty:
        raise ValueError("PoB2 must be a clean checkout of the manifest revision")
    name = f"exileai-spike-{uuid4().hex}"
    command = [
        "docker",
        "run",
        "--rm",
        "--name",
        name,
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
        "CI=true",
        "--env",
        "LUA_PATH=../runtime/lua/?.lua;../runtime/lua/?/init.lua;;",
        "-i",
        runtime["image"],
        "luajit",
        "/workspace/scripts/pob_spike.lua",
    ]
    started = time.perf_counter()
    try:
        process = subprocess.run(
            command,
            input=json.dumps(request, allow_nan=False),
            text=True,
            capture_output=True,
            timeout=180,
            check=False,
        )
    finally:
        try:
            subprocess.run(
                ["docker", "rm", "-f", name],
                capture_output=True,
                timeout=15,
                check=False,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print(f"Could not confirm cleanup of {name}", file=sys.stderr)
    records = [
        line.removeprefix("EXILEAI_RESULT=")
        for line in process.stdout.splitlines()
        if line.startswith("EXILEAI_RESULT=")
    ]
    diagnostics = "\n".join(
        line
        for line in process.stdout.splitlines()
        if not line.startswith("EXILEAI_RESULT=")
    )
    print(diagnostics, file=sys.stderr)
    print(process.stderr, file=sys.stderr)
    if process.returncode or len(records) != 1:
        raise RuntimeError("PoB2 experiment failed; inspect stderr diagnostics")
    result: dict[str, Any] = json.loads(records[0])
    if "audited_xml" in result:
        validate_fixed_inputs(result["audited_xml"], result["modified_xml"])
    result["runtime"] = runtime
    result["objective"] = request.get("objective")
    result["wall_seconds"] = time.perf_counter() - started
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--create-fixture", action="store_true")
    parser.add_argument("--code", type=Path)
    parser.add_argument("--request", type=Path)
    args = parser.parse_args()
    if args.create_fixture:
        request = {"operation": "create_fixture"}
    else:
        if not args.code or not args.request:
            parser.error("Provide --code and --request, or --create-fixture")
        request = json.loads(args.request.read_text())
        request["xml"] = decode_build_code(args.code.read_text())
    result = run_experiment(request)
    if args.create_fixture:
        result["code"] = encode_build_xml(result["xml"])
        result["xml_sha256"] = hashlib.sha256(result["xml"].encode()).hexdigest()
    else:
        for field in ("original_xml", "audited_xml", "modified_xml"):
            if field not in result:
                continue
            result[field + "_sha256"] = hashlib.sha256(
                result.pop(field).encode()
            ).hexdigest()
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

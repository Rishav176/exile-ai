"""Report prerequisites without changing machine configuration."""

import json
import platform
import shutil
import subprocess
import sys


def main() -> int:
    results: dict[str, object] = {"python": platform.python_version()}
    ready = sys.version_info[:2] == (3, 12)
    for command in ("git", "docker"):
        executable = shutil.which(command)
        results[command] = executable
        ready = ready and executable is not None
    if shutil.which("docker"):
        try:
            probe = subprocess.run(
                ["docker", "info", "--format", "{{.OSType}}"],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            results["docker_server_os"] = probe.stdout.strip()
            results["docker_error"] = probe.stderr.strip()
            ready = ready and probe.returncode == 0 and probe.stdout.strip() == "linux"
        except subprocess.TimeoutExpired:
            results["docker_error"] = "Docker server check timed out"
            ready = False
    results["ready"] = ready
    print(json.dumps(results, indent=2))
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())

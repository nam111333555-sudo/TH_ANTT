"""Temporary working directory runner; optional Docker isolation.

The process backend is for trusted lab commands. A temporary cwd is NOT a
security boundary. Use backend='docker' for container-level restrictions.
"""
from pathlib import Path
import shlex
import subprocess
import tempfile


class VirtualSandbox:
    def __init__(self, backend="process", timeout=5, image="python:3.14-slim"):
        if backend not in {"process", "docker"}:
            raise ValueError("Unknown sandbox backend")
        self.backend = backend
        self.timeout = timeout
        self.image = image
        self._temp = tempfile.TemporaryDirectory(prefix="lab05-")
        self.temp_dir = self._temp.name
        self.returncode = None

    def run_isolated(self, command):
        args = shlex.split(command) if isinstance(command, str) else command
        if not isinstance(args, list) or not args or not all(
                isinstance(arg, str) and arg and "\0" not in arg for arg in args):
            raise ValueError("command must contain nonempty string arguments")
        # echo is a shell builtin on Windows; implement this harmless demo directly.
        if args[0] == "echo" and self.backend == "process":
            self.returncode = 0
            return " ".join(args[1:]) + "\n", ""
        container_name = "lab05-" + Path(self.temp_dir).name
        if self.backend == "docker":
            args = ["docker", "run", "--rm", "--pull=never", "--name", container_name,
                    "--network=none", "--read-only", "--memory=128m", "--cpus=0.5",
                    "--pids-limit=32", "--cap-drop=ALL",
                    "--security-opt=no-new-privileges", "--user=65534:65534",
                    "--tmpfs=/tmp:rw,noexec,nosuid,size=16m", self.image, *args]
        try:
            result = subprocess.run(args, cwd=self.temp_dir, capture_output=True,
                                    text=True, encoding="utf-8", errors="replace",
                                    shell=False, timeout=self.timeout)
        except subprocess.TimeoutExpired:
            if self.backend == "docker":
                subprocess.run(["docker", "rm", "-f", container_name],
                               capture_output=True, timeout=10)
            raise
        self.returncode = result.returncode
        return result.stdout, result.stderr

    def close(self):
        self._temp.cleanup()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

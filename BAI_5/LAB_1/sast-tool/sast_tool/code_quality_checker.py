import re
import subprocess
import sys


class CodeQualityChecker:
    def check(self, filepath):
        result = subprocess.run(
            [sys.executable, "-m", "flake8", "--isolated", str(filepath)],
            capture_output=True, text=True, encoding="utf-8", timeout=30)
        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr.strip() or result.stdout.strip())
        issues = []
        for line in result.stdout.splitlines():
            # Greedy path group handles the drive colon in Windows paths.
            match = re.match(r"^(.*):(\d+):(\d+):\s*(.*)$", line)
            if match:
                issues.append({"type": "Lint Issue", "message": match[4],
                               "lineno": int(match[2]),
                               "col_offset": int(match[3]) - 1,
                               "severity": "low"})
        return issues

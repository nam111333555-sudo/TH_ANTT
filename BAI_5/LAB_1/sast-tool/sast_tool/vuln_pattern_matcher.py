import ast
import re


class VulnPatternMatcher:
    """Structural defaults avoid matches inside comments and string literals.

    Optional regex patterns use the same pattern/message format as the handout.
    """

    def __init__(self, patterns=None):
        self.patterns = patterns or []

    def match(self, code: str):
        issues = []
        lines = code.splitlines()
        for node in ast.walk(ast.parse(code)):
            message = None
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                if (isinstance(node.value, ast.Constant)
                        and isinstance(node.value.value, str) and node.value.value
                        and any(isinstance(t, ast.Name) and "password" in t.id.lower()
                                for t in targets)):
                    message = "Hardcoded password detected (including demo credentials)."
            if isinstance(node, ast.Import) and any(a.name == "pickle" for a in node.names):
                message = "Usage of pickle module can be unsafe with untrusted data."
            if isinstance(node, ast.ImportFrom) and node.module == "pickle":
                message = "Usage of pickle module can be unsafe with untrusted data."
            if message:
                column = len(lines[node.lineno - 1].encode("utf-8")[:node.col_offset]
                             .decode("utf-8"))
                issues.append({"type": "Pattern Match", "message": message,
                               "lineno": node.lineno, "col_offset": column})
        for pattern in self.patterns:
            for match in re.finditer(pattern["pattern"], code):
                start = match.start()
                issues.append({
                    "type": "Pattern Match", "message": pattern["message"],
                    "lineno": code.count("\n", 0, start) + 1,
                    "col_offset": start - code.rfind("\n", 0, start) - 1,
                })
        return sorted(issues, key=lambda i: (i["lineno"], i["col_offset"]))

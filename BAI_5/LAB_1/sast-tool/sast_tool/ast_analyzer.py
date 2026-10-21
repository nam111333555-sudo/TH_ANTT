"""Inspect syntax without executing the submitted program."""
import ast


class ASTAnalyzer:
    def analyze(self, code: str):
        tree = ast.parse(code)
        issues = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                name = node.func.id
                issues.append({
                    "type": f"Use of {name}",
                    "message": f"Use of {name}() can execute untrusted code.",
                    "lineno": node.lineno,
                    "col_offset": len(code.splitlines()[node.lineno - 1]
                                      .encode("utf-8")[:node.col_offset]
                                      .decode("utf-8")),
                })
        return issues

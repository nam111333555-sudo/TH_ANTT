import json
from pathlib import Path


class SecurityRuleEngine:
    def __init__(self, rules_file=None):
        path = Path(rules_file) if rules_file else (
            Path(__file__).resolve().parents[1] / "rules" / "default_rules.json")
        self.rules = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(self.rules, list) or any(
                not isinstance(r, dict) or not isinstance(r.get("type"), str)
                or r.get("severity", "medium") not in {"low", "medium", "high"}
                for r in self.rules):
            raise ValueError("Rules must be a list of type/severity objects.")

    def evaluate(self, ast_issues, pattern_issues):
        severities = {r["type"]: r.get("severity", "medium") for r in self.rules}
        return [dict(issue, severity=severities.get(issue["type"], "medium"))
                for issue in ast_issues + pattern_issues]

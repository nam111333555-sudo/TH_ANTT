"""Serialize SARIF 2.1.0 using standard JSON (no object metadata)."""
import json
from pathlib import Path


class SarifReporter:
    def generate_report(self, issues, output_file="report.sarif", analyzed_file="input.py"):
        uri = Path(analyzed_file).resolve().as_uri()
        rule_ids = list(dict.fromkeys(i["type"] for i in issues))
        levels = {"high": "error", "medium": "warning", "low": "note"}
        report = {
            "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
            "version": "2.1.0",
            "runs": [{
                "tool": {"driver": {"name": "PySAST", "version": "1.0.0",
                                    "rules": [{"id": r} for r in rule_ids]}},
                "columnKind": "unicodeCodePoints",
                "results": [{
                    "ruleId": i["type"],
                    "level": levels.get(i.get("severity"), "warning"),
                    "message": {"text": i["message"]},
                    "locations": [{"physicalLocation": {
                        "artifactLocation": {"uri": uri},
                        "region": {"startLine": i["lineno"],
                                   "startColumn": i["col_offset"] + 1},
                    }}],
                } for i in issues],
            }],
        }
        Path(output_file).write_text(json.dumps(report, ensure_ascii=False, indent=2),
                                     encoding="utf-8")
        return report

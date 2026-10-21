import json
from pathlib import Path
import tempfile
import unittest

from sast_tool.security_rule_engine import SecurityRuleEngine


class TestSecurityRuleEngine(unittest.TestCase):
    def test_severities_and_no_mutation(self):
        issues = [{"type": "Use of eval"}, {"type": "Pattern Match"}]
        result = SecurityRuleEngine().evaluate(issues[:1], issues[1:])
        self.assertEqual([i["severity"] for i in result], ["high", "medium"])
        self.assertNotIn("severity", issues[0])

    def test_custom_rules(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "rules.json"
            path.write_text(json.dumps([{"type": "Custom", "severity": "low"}]))
            engine = SecurityRuleEngine(path)
            self.assertEqual(engine.evaluate([{"type": "Custom"}], [])[0]["severity"],
                             "low")

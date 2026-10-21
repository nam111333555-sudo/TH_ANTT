import json
from pathlib import Path
import tempfile
import unittest

from sast_tool.sarif_reporter import SarifReporter


class TestSarifReporter(unittest.TestCase):
    def test_report_location_and_severity(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "report.sarif"
            source = Path(folder) / "code with spaces.py"
            issues = [{"type": "Use of eval", "message": "Danger", "lineno": 2,
                       "col_offset": 4, "severity": "high"}]
            SarifReporter().generate_report(issues, path, source)
            report = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(report["version"], "2.1.0")
            result = report["runs"][0]["results"][0]
            self.assertEqual(result["level"], "error")
            location = result["locations"][0]["physicalLocation"]
            self.assertEqual(location["region"], {"startLine": 2, "startColumn": 5})
            self.assertEqual(location["artifactLocation"]["uri"], source.as_uri())

    def test_empty_report(self):
        with tempfile.TemporaryDirectory() as folder:
            result = SarifReporter().generate_report([], Path(folder) / "empty.sarif")
            self.assertEqual(result["runs"][0]["results"], [])

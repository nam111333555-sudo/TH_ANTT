from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from sast_tool.code_quality_checker import CodeQualityChecker


class TestCodeQualityChecker(unittest.TestCase):
    def test_real_flake8_detection(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sample.py"
            path.write_text("import os\n", encoding="utf-8")
            issues = CodeQualityChecker().check(path)
            self.assertTrue(any("F401" in i["message"] for i in issues))
            self.assertEqual(issues[0]["col_offset"], 0)

    @patch("sast_tool.code_quality_checker.subprocess.run")
    def test_windows_drive_and_message_colon(self, run):
        run.return_value = subprocess.CompletedProcess(
            [], 1, "D:\\work\\test.py:3:5: E999 SyntaxError: bad syntax\n", "")
        issue = CodeQualityChecker().check("unused")[0]
        self.assertEqual((issue["lineno"], issue["col_offset"]), (3, 4))
        self.assertIn("SyntaxError: bad syntax", issue["message"])

    @patch("sast_tool.code_quality_checker.subprocess.run")
    def test_missing_dependency_is_not_clean_result(self, run):
        run.return_value = subprocess.CompletedProcess([], 2, "", "No module flake8")
        with self.assertRaises(RuntimeError):
            CodeQualityChecker().check("unused")

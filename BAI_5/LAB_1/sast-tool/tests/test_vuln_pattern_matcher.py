import unittest

from sast_tool.vuln_pattern_matcher import VulnPatternMatcher


class TestVulnPatternMatcher(unittest.TestCase):
    def test_password_and_pickle(self):
        code = "password = 'DEMO_ONLY'\nimport pickle\nfrom pickle import loads"
        issues = VulnPatternMatcher().match(code)
        self.assertEqual([i["lineno"] for i in issues], [1, 2, 3])
        self.assertTrue(all(i["type"] == "Pattern Match" for i in issues))

    def test_comments_and_strings_are_ignored(self):
        self.assertEqual(VulnPatternMatcher().match(
            "# password = 'x'\ns = 'import pickle'\npassword = None"), [])

    def test_custom_pattern_column(self):
        matcher = VulnPatternMatcher([{"pattern": "danger", "message": "custom"}])
        issue = matcher.match("# danger")[0]
        self.assertEqual((issue["lineno"], issue["col_offset"]), (1, 2))

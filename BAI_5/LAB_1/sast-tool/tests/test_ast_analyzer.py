import unittest

from sast_tool.ast_analyzer import ASTAnalyzer


class TestASTAnalyzer(unittest.TestCase):
    def test_detect_eval_and_exec(self):
        issues = ASTAnalyzer().analyze("eval('2+2')\nexec('x=1')")
        self.assertEqual([i["type"] for i in issues], ["Use of eval", "Use of exec"])
        self.assertEqual([i["lineno"] for i in issues], [1, 2])

    def test_no_false_positive_in_comments_or_attributes(self):
        self.assertEqual(ASTAnalyzer().analyze("# eval('x')\nobj.eval('x')"), [])

    def test_unicode_column(self):
        issue = ASTAnalyzer().analyze("x = 'ễ'; eval('2')")[0]
        self.assertEqual(issue["col_offset"], 9)

    def test_invalid_syntax(self):
        with self.assertRaises(SyntaxError):
            ASTAnalyzer().analyze("def (")

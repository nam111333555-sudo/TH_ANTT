import argparse
from pathlib import Path
import tokenize

from sast_tool.ast_analyzer import ASTAnalyzer
from sast_tool.code_quality_checker import CodeQualityChecker
from sast_tool.sarif_reporter import SarifReporter
from sast_tool.security_rule_engine import SecurityRuleEngine
from sast_tool.vuln_pattern_matcher import VulnPatternMatcher


def main(file_path, output="report.sarif", rules=None):
    with tokenize.open(file_path) as source:
        code = source.read()
    issues = SecurityRuleEngine(rules).evaluate(
        ASTAnalyzer().analyze(code), VulnPatternMatcher().match(code))
    issues += CodeQualityChecker().check(Path(file_path).resolve())
    issues.sort(key=lambda i: (i["lineno"], i["col_offset"], i["type"]))
    SarifReporter().generate_report(issues, output, file_path)
    print(f"Analysis complete: {len(issues)} issues. Report saved to {output}")
    return issues


def cli():
    parser = argparse.ArgumentParser(description="Lab 05 Python SAST")
    parser.add_argument("file", type=Path)
    parser.add_argument("-o", "--output", default="report.sarif")
    parser.add_argument("--rules", type=Path)
    args = parser.parse_args()
    try:
        main(args.file, args.output, args.rules)
    except (OSError, SyntaxError, ValueError, RuntimeError) as exc:
        parser.exit(2, f"Analysis failed: {exc}\n")


if __name__ == "__main__":
    cli()

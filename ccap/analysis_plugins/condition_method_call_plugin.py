from plugin_definition.abstract_analysis_plugin import AbstractAnalysisPlugin
from reporting.analysis_results import AbstractAnalysisProblem, AnalysisReport
from plugin_definition.plugin_meta_data import PluginMetaData
import ast
from typing import List
from components.input_component import ParsedSourceFile

class ConditionMethodCallPlugin(AbstractAnalysisPlugin):
    def __init__(self):
        self.metadata = PluginMetaData(
            name="Condition Method Call Plugin",
            author="Enrico Kaack <e.kaack@live.de>"
        )

    def do_analysis(self, source_files: List[ParsedSourceFile]) -> AnalysisReport:
        report = AnalysisReport(self.metadata)

        for source_file in source_files:
            problem_in_ast = self._analyse_single_ast(source_file)
            report.problems.extend(problem_in_ast)

        return report

    def _analyse_single_ast(self, a):

        problems = []
        for node in ast.walk(a.ast):
            # for all if
            if isinstance(node, ast.If):
                testNode = node.test

                if self._check_if_direct_comparison(testNode):
                    problems.append(ExplicitComparisonInConditionProblem(a.file_path, testNode.lineno))
        return problems

    def _check_if_direct_comparison(self, node):
        if isinstance(node, ast.BoolOp):
            violated = False
            #check all expressions of the boolean operator
            for value in node.values:
                if self._check_if_direct_comparison(value):
                    violated = True
            return violated
        elif isinstance(node, ast.UnaryOp):
            return self._check_if_direct_comparison(node.operand)

        return not isinstance(node, ast.Call)


class ExplicitComparisonInConditionProblem(AbstractAnalysisProblem):
    def __init__(self, file_path, line_number):
        self.name = "Explicit comparison in condition"
        self.description = "Explicit comparisons in condition statements should be replaced by method call for better readability."
        super().__init__(file_path, line_number)


def test_condition_comparison_found():
    code = "def f():\n\tif a < b:\n\t\treturn 5"
    path = "test_path"
    parsed_ast = ast.parse(code, path)
    p = ParsedSourceFile(path, parsed_ast, code)

    plugin = ConditionMethodCallPlugin()
    analysis_report = plugin.do_analysis([p])
    assert len(analysis_report.problems) == 1
    assert analysis_report.problems[0].name == "Explicit comparison in condition"
    assert analysis_report.problems[0].file_path == "test_path"
    assert analysis_report.problems[0].line_number == 2

def test_condition_comparison_nested_found():
    code = "def f():\n\tif isSmaller(a,b) or isBigger(a,b) and not a <b:\n\t\treturn 5"
    path = "test_path"
    parsed_ast = ast.parse(code, path)
    p = ParsedSourceFile(path, parsed_ast, code)

    plugin = ConditionMethodCallPlugin()
    analysis_report = plugin.do_analysis([p])
    assert len(analysis_report.problems) == 1
    assert analysis_report.problems[0].name == "Explicit comparison in condition"
    assert analysis_report.problems[0].file_path == "test_path"
    assert analysis_report.problems[0].line_number == 2

def test_condition_comparison_not_found():
    code = "def f():\n\tif isSmaller(a,b):\n\t\treturn 5"
    path = "test_path"
    parsed_ast = ast.parse(code, path)
    p = ParsedSourceFile(path, parsed_ast, code)

    plugin = ConditionMethodCallPlugin()
    analysis_report = plugin.do_analysis([p])
    assert len(analysis_report.problems) == 0
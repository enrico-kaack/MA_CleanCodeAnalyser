from plugin_definition.abstract_analysis_plugin import AbstractAnalysisPlugin
from reporting.analysis_results import AbstractAnalysisProblem, AnalysisReport
from plugin_definition.plugin_meta_data import PluginMetaData
import ast
from typing import List
from components.input_component import ParsedSourceFile


class ConditionMethodCallPluginSimple(AbstractAnalysisPlugin):
    def __init__(self):
        self.metadata = PluginMetaData(
            name="Simple Condition Method Call Plugin",
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

                if isinstance(testNode, ast.Compare):
                    problems.append(ExplicitComparisonInConditionProblem(a.file_path, testNode.lineno))
        return problems


class ExplicitComparisonInConditionProblem(AbstractAnalysisProblem):
    def __init__(self, file_path, line_number):
        self.name = "Explicit comparison in condition simple"
        self.description = "Explicit comparisons in conditions should be replaced by method call for better readability"
        super().__init__(file_path, line_number)


def test_condition_comparison_simple_found():
    code = "def f():\n\tif a < b:\n\t\treturn 5"
    path = "test_path"
    parsed_ast = ast.parse(code, path)
    p = ParsedSourceFile(path, parsed_ast, code)

    plugin = ConditionMethodCallPluginSimple()
    analysis_report = plugin.do_analysis([p])
    assert len(analysis_report.problems) == 1
    assert analysis_report.problems[0].name == "Explicit comparison in condition simple"
    assert analysis_report.problems[0].file_path == "test_path"
    assert analysis_report.problems[0].line_number == 2

def test_condition_comparison_simple_is_comparison():
    code = "def f():\n\tif a is 5:\n\t\treturn 5"
    path = "test_path"
    parsed_ast = ast.parse(code, path)
    p = ParsedSourceFile(path, parsed_ast, code)

    plugin = ConditionMethodCallPluginSimple()
    analysis_report = plugin.do_analysis([p])
    assert len(analysis_report.problems) == 1
    assert analysis_report.problems[0].name == "Explicit comparison in condition simple"
    assert analysis_report.problems[0].file_path == "test_path"
    assert analysis_report.problems[0].line_number == 2

def test_condition_comparison_simple_is_not():
    code = "def f():\n\tif a is not 5:\n\t\treturn 5"
    path = "test_path"
    parsed_ast = ast.parse(code, path)
    p = ParsedSourceFile(path, parsed_ast, code)

    plugin = ConditionMethodCallPluginSimple()
    analysis_report = plugin.do_analysis([p])
    assert len(analysis_report.problems) == 1
    assert analysis_report.problems[0].name == "Explicit comparison in condition simple"
    assert analysis_report.problems[0].file_path == "test_path"
    assert analysis_report.problems[0].line_number == 2

def test_condition_comparison_simple_not():
    code = "def f():\n\tif not a < 5:\n\t\treturn 5"
    path = "test_path"
    parsed_ast = ast.parse(code, path)
    p = ParsedSourceFile(path, parsed_ast, code)

    plugin = ConditionMethodCallPluginSimple()
    analysis_report = plugin.do_analysis([p])
    assert len(analysis_report.problems) == 0

def test_condition_comparison_simple_and():
    code = "def f():\n\tif a < 5 and b < 2:\n\t\treturn 5"
    path = "test_path"
    parsed_ast = ast.parse(code, path)
    p = ParsedSourceFile(path, parsed_ast, code)

    plugin = ConditionMethodCallPluginSimple()
    analysis_report = plugin.do_analysis([p])
    assert len(analysis_report.problems) == 0
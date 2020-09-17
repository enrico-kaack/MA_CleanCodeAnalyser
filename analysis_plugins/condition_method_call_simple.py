from plugin_definition.abstract_analysis_plugin import AbstractAnalysisPlugin
from reporting.analysis_results import AbstractAnalysisProblem, AnalysisReport
from plugin_definition.plugin_meta_data import PluginMetaData
import ast
from typing import List
from ast_parser import ParsedSourceFile


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

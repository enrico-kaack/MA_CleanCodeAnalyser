from analysis_plugin_handler.abstract_analysis_plugin import AbstractAnalysisPlugin
from reporting.analysis_results import AbstractAnalysisProblem, AnalysisReport
from reporting.plugin_meta_data import PluginMetaData
import ast
from helper import ast_pretty_print

class ConditionMethodCallPluginSimple(AbstractAnalysisPlugin):
    def __init__(self):
        super().__init__()

        self.metadata = PluginMetaData(
            name="Simple Condition Method Call Plugin",
            author="Enrico Kaack <e.kaack@live.de>"
        )

    def do_analysis(self, asts):
        report = AnalysisReport(self.metadata)
        
        for a in asts:
            problem_in_ast = self.analyse_single_ast(a)
            report.problems.extend(problem_in_ast)

        return report

    def analyse_single_ast(self, a):
        problems = []
        for node in ast.walk(a.ast):
            #for all if
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
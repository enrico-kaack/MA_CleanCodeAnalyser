from plugin_definition.abstract_analysis_plugin import AbstractAnalysisPlugin
from reporting.analysis_results import AbstractAnalysisProblem, AnalysisReport
from plugin_definition.plugin_meta_data import PluginMetaData
import ast
from helper import ast_pretty_print

class ConditionMethodCallPlugin(AbstractAnalysisPlugin):
    def __init__(self):
        super().__init__()

        self.metadata = PluginMetaData(
            name="Condition Method Call Plugin",
            author="Enrico Kaack <e.kaack@live.de>"
        )

    def do_analysis(self, source_files):
        report = AnalysisReport(self.metadata)
        
        for source_file in source_files:
            problem_in_ast = self.analyse_single_ast(source_file)
            report.problems.extend(problem_in_ast)

        return report

    def analyse_single_ast(self, a):

        problems = []
        for node in ast.walk(a.ast):
            #for all if
            if isinstance(node, ast.If):
                testNode = node.test

                if self._check_if_direct_comparison(testNode):
                    problems.append(ExplicitComparisonInConditionProblem(a.file_path, testNode.lineno))
        return problems

    def _check_if_direct_comparison(self, node):
        if isinstance(node, ast.BoolOp):
            violated = False
            for n in node.values:
                if self._check_if_direct_comparison(n):
                    violated = True
            return violated
        if isinstance(node, ast.UnaryOp):
            return self._check_if_direct_comparison(node.operand)
        if not  isinstance(node, ast.Call):
            return True
    


class ExplicitComparisonInConditionProblem(AbstractAnalysisProblem):
    def __init__(self, file_path, line_number):
        self.name = "Explicit comparison in condition"
        self.description = "Explicit comparisons in conditions should be replaced by method call for better readability"
        super().__init__(file_path, line_number)
from analysis_plugin_handler.abstract_analysis_plugin import AbstractAnalysisPlugin
from reporting.analysis_results import AbstractAnalysisProblem, AnalysisReport
from reporting.plugin_meta_data import PluginMetaData
import ast
from helper import ast_pretty_print

class ConditionMethodCallPlugin(AbstractAnalysisPlugin):
    def __init__(self):
        super().__init__()

        self.metadata = PluginMetaData(
            name="Return None (Null) Plugin",
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
            if isinstance(node, ast.Return):
                return_value = node.value
                if isinstance(return_value, ast.Constant):
                    if return_value.value == None:
                        problems.append(ReturnNullProblem(a.file_path, return_value.lineno))
        return problems

    


class ReturnNullProblem(AbstractAnalysisProblem):
    def __init__(self, file_path, line_number):
        self.name = "Returned None"
        self.description = "Returning None is dangerous, since the caller has to check for None. Otherwise, a runtime exception can occur."
        super().__init__(file_path, line_number)
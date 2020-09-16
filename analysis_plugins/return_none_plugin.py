from plugin_definition.abstract_analysis_plugin import AbstractAnalysisPlugin
from reporting.analysis_results import AbstractAnalysisProblem, AnalysisReport
from plugin_definition.plugin_meta_data import PluginMetaData
import ast
from helper import ast_pretty_print


class ReturnNonePlugin(AbstractAnalysisPlugin):
    def __init__(self):
        super().__init__()

        self.metadata = PluginMetaData(
            name="Return None (Null) Plugin",
            author="Enrico Kaack <e.kaack@live.de>"
        )

    def do_analysis(self, source_files):
        report = AnalysisReport(self.metadata)

        for source_file in source_files:
            problem_in_ast = self._analyse_single_ast(source_file)
            report.problems.extend(problem_in_ast)

        return report

    def _analyse_single_ast(self, a):
        problems = []
        for node in ast.walk(a.ast):
            if isinstance(node, ast.Return):
                return_value = node.value
                if isinstance(return_value, ast.Constant) or isinstance(return_value, ast.NameConstant):
                    if return_value.value is None:
                        problems.append(ReturnNullProblem(a.file_path, return_value.lineno))
        return problems




class ReturnNullProblem(AbstractAnalysisProblem):
    def __init__(self, file_path, line_number):
        self.name = "Returned None"
        self.description = "Returning None is dangerous, since the caller has to check for None. Otherwise, a runtime exception may occur."
        super().__init__(file_path, line_number)
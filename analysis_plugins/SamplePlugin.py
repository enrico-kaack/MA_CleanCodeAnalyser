from analysis_plugin_handler.abstract_analysis_plugin import AbstractAnalysisPlugin
from reporting.analysis_results import AbstractAnalysisProblem, AnalysisReport
from reporting.plugin_meta_data import PluginMetaData

class SamplePlugin(AbstractAnalysisPlugin):
    def __init__(self):
        super().__init__()

        self.metadata = PluginMetaData(
            name="Sample Plugin",
            author="Enrico Kaack <e.kaack@live.de>"
        )

    def doAnalysis(self, ast):
        print("Doing work", self.metadata.name)

        report = AnalysisReport(self.metadata)
        
        # Sample problem
        problem1 = SampleProblem(1, 12)
        report.append_problem(problem1)
        return report


class SampleProblem(AbstractAnalysisProblem):
    def __init__(self, file_path, line_number):
        self.name = "Sample Problem that describes bad behaviour"
        self.description = "describes why this problem is bad coding practise"
        super().__init__(file_path, line_number)
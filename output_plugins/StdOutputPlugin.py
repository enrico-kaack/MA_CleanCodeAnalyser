from analysis_plugin_handler.abstract_output_plugin import AbstractOutputPlugin
from reporting.plugin_meta_data import PluginMetaData
from reporting.analysis_results import FullReport, AnalysisReport

from functools import reduce

class StdOutputPlugin(AbstractOutputPlugin):
    def __init__(self):
        super().__init__()
        self.output_format = "std"

        self.metadata = PluginMetaData(
            name="Standard Output Plugin",
            author="Enrico Kaack <e.kaack@live.de>"
        )

    def write_report(self, full_report : FullReport):
        output_str = f"""
        Analysis Report on {full_report.run_arguments.input_directory}.
        Analyse Plugins: {", ".join([p.plugin_metadata.name for p in full_report.reports])}.
        Total time: {full_report.analysis_time}
        Summary: Found {len([r1 for r in full_report.reports for r1 in r.problems])} problem(s)
        ----------------------------------------
        RESULTS:"""
        
        for plugin_report in full_report.reports:
            output_str += f"""
            PLUGIN NAME: {plugin_report.plugin_metadata.name} by {plugin_report.plugin_metadata.author}"""
            for problem in plugin_report.problems:
                output_str += f"""
                Found {problem.name} ({problem.file_path}:{problem.line_number})
                    {problem.description}
                """
        print(output_str)



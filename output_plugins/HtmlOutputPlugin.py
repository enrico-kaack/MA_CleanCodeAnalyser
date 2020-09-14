from plugin_definition.abstract_output_plugin import AbstractOutputPlugin
from plugin_definition.plugin_meta_data import PluginMetaData
from reporting.analysis_results import FullReport, AnalysisReport

from functools import reduce

class StdOutputPlugin(AbstractOutputPlugin):
    def __init__(self):
        super().__init__()
        self.output_format = "html"

        self.metadata = PluginMetaData(
            name="HTML Output Plugin",
            author="Enrico Kaack <e.kaack@live.de>"
        )

    def handle_report(self, full_report : FullReport):
        output_str = f"""
        <html>
        <head>
        <title>Analysis Report</title>
        </head>
        <body>
        <h1>Analysis Report on {full_report.run_arguments.input_directory}</h1>
        <h2>Loaded Analyse Plugins: </h2>
        <div>{", ".join([p.plugin_metadata.name for p in full_report.reports])}.</div>
        <h2>Summary</h2>
        <div>Total Time:  {full_report.analysis_time}s </div>
        <div>{len([r1 for r in full_report.reports for r1 in r.problems])} problem(s) found </div>
        <h2>RESULTS</h2>"""
        
        for plugin_report in full_report.reports:

            for problem in plugin_report.problems:
                output_str += f"""
                <h3 title="{problem.description} from {plugin_report.plugin_metadata.name}">{problem.name} </h3>
                <span> in {problem.file_path}:{problem.line_number}</span>
                   
                """
        output_str += "</body></html>"
        with open("report.html", "x") as output_file:
            output_file.write(output_str) 



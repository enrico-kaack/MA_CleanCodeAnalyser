from ccap.plugin_definition.abstract_output_plugin import AbstractOutputPlugin
from ccap.plugin_definition.plugin_meta_data import PluginMetaData
from ccap.reporting.analysis_results import FullReport
from jinja2 import Template


class HtmlOutputPlugin(AbstractOutputPlugin):
    def __init__(self):
        super().__init__()
        self.output_format = "html"

        self.metadata = PluginMetaData(
            name="HTML Output Plugin",
            author="Enrico Kaack <e.kaack@live.de>"
        )

    def handle_report(self, full_report: FullReport):
        with open("output_plugins/report-template.html", "r") as template_file:
            template = Template(template_file.read())
            output_str = template.render(location=full_report.run_arguments.input_directory, plugins=", ".join([p.plugin_metadata.name for p in full_report.reports]), total_time=full_report.analysis_time,
            no_problems_found=len([r1 for r in full_report.reports for r1 in r.problems]), reports=full_report.reports)
            with open("report.html", "x") as output_file:
                output_file.write(output_str) 

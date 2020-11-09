from ccap.components.analysis_plugin_handler import AnalysisPluginHandler
from ccap.components.output_plugin_handler import OutputPluginHandler
from ccap.components.input_component import parse_ast_from_folder
from ccap.helper.input_arguments import Arguments

class CoreComponent():
    def __init__(self):
        self.analysis_plugin_handler = None
        self.output_plugin_handler = None
        self.args = None

    def run(self):
        self._parse_arguments()

        self._init_components()

        self._execute_analysis()

    def _parse_arguments(self):
        self.args = Arguments()

    def _init_components(self):
        self.analysis_plugin_handler = AnalysisPluginHandler(self.args)
        self.output_plugin_handler = OutputPluginHandler(self.args)

    def _execute_analysis(self):
        # get asts for all files
        parsed_files = parse_ast_from_folder(self.args.input_directory)

        # perform analysis
        full_report = self.analysis_plugin_handler.apply_all_plugins_on(parsed_files)

        # output result
        self.output_plugin_handler.apply_output_plugin_as_specified_in_arguments(full_report)

    
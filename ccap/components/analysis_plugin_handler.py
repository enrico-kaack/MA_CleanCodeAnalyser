from ccap.plugin_definition.abstract_analysis_plugin import AbstractAnalysisPlugin
from ccap.reporting.analysis_results import FullReport
from ccap.helper.plugin_loader import load_plugins_with_symlinking
import time
import logging
from typing import List

class AnalysisPluginHandler(object):
    plugins: List[AbstractAnalysisPlugin] = []

    def __init__(self, run_arguments):
        self.run_arguments = run_arguments
        self.load_plugins()

    def load_plugins(self):
        self.plugins = load_plugins_with_symlinking(plugin_type=AbstractAnalysisPlugin, own_directory="ccap.analysis_plugins", custom_directory=self.run_arguments.analysis_plugin_directory )

    def apply_all_plugins_on(self, source_files):
        """Apply all of the plugins on the argument supplied to this function
        """
        full_report = FullReport(run_arguments=self.run_arguments)
        start = time.perf_counter()
        for plugin in self.plugins:
            logging.debug(f'    Applying {plugin.metadata.name}')
            report = plugin.do_analysis(source_files)
            full_report.append_report(report)
        end = time.perf_counter()
        full_report.analysis_time = end - start

        return full_report
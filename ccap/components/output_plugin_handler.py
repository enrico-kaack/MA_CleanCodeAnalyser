from ccap.plugin_definition.abstract_output_plugin import AbstractOutputPlugin
from ccap.helper.plugin_loader import load_plugins_with_symlinking
import logging
from typing import Optional

class OutputPluginHandler(object):
    output_plugin: Optional[AbstractOutputPlugin] = None

    def __init__(self, run_arguments):
        self.run_arguments = run_arguments
        self.load_plugins()

    def load_plugins(self):
        self.plugins = load_plugins_with_symlinking(plugin_type=AbstractOutputPlugin, own_directory="ccap.output_plugins", custom_directory=self.run_arguments.output_plugin_directory )
        self. _select_specified_output_plugin()

    def _select_specified_output_plugin(self):
        self.output_plugin = next((plugin for plugin in self.plugins if plugin.output_format == self.run_arguments.output), None)
        assert self.output_plugin is not None, f"The specified output plugin {self.run_arguments.output} is not found in {','.join([plugin.output_format for plugin in self.plugins])}"

    def apply_output_plugin_as_specified_in_arguments(self, full_report):
        """apply the plugin corresponding to the value specified as run argument
        """
        logging.debug(f'    Applying Output {self.output_plugin.metadata.name}')
        self.output_plugin.handle_report(full_report)

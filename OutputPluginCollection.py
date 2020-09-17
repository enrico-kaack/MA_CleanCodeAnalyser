from plugin_definition.abstract_output_plugin import AbstractOutputPlugin
from plugin_loader import load_plugins

class OutputPluginCollection(object):


    def __init__(self, run_arguments):
        self.run_arguments = run_arguments
        self.load_plugins()

    def load_plugins(self):
        self.plugins = load_plugins(plugin_type=AbstractOutputPlugin, directory=self.run_arguments.output_plugin_directory )
        self. _select_specified_output_plugin()

    def _select_specified_output_plugin(self):
        self.output_plugin = next((plugin for plugin in self.plugins if plugin.output_format == self.run_arguments.output), None)
        assert self.output_plugin is not None, f"The specified output plugin {self.run_arguments.output} is not found in {','.join([plugin.output_format for plugin in self.plugins])}"

    def apply_output_plugin_as_specified_in_arguments(self, full_report):
        """apply the plugin corresponding to the value specified as run argument
        """
        print(f'    Applying Output {self.output_plugin.metadata.name}')
        self.output_plugin.handle_report(full_report)

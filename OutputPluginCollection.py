import pkgutil
import inspect
from plugin_definition.abstract_output_plugin import AbstractOutputPlugin
from reporting.analysis_results import FullReport

class OutputPluginCollection(object):

    def __init__(self, run_arguments):
        self.run_arguments = run_arguments
        self.load_plugins()


    def load_plugins(self):
        self.plugins = []
        self.seen_paths = []
        print(f'Searching plugins in {self.run_arguments.output_plugin_directory}')
        self._walk_package(self.run_arguments.output_plugin_directory)

    def _walk_package(self, package):
        """Walk the package and get all plugins. 
        """
        imported_package = __import__(package, fromlist=[''])

        for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not ispkg:
                print("importing pluginname", pluginname)
                plugin_module = __import__(pluginname, fromlist=[''])
                clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
                for (_, c) in clsmembers:
                    # Only add classes that are a sub class of Plugin, but NOT Plugin itself
                    if issubclass(c, AbstractOutputPlugin) & (c is not AbstractOutputPlugin):
                        print(f'    Found plugin: {c.__module__}.{c.__name__}')
                        self.plugins.append(c())

    def apply_output_plugin_as_specified_in_arguments(self, full_report):
        """apply the plugin corresponding to the value specified as run argument
        """

        for plugin in self.plugins:
            if plugin.output_format == self.run_arguments.output:
                print(f'    Applying Output {plugin.metadata.name}')
                plugin.write_report(full_report)

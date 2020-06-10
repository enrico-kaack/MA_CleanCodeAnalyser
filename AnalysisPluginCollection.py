import pkgutil
import inspect
import ast
from analysis_plugin_handler.abstract_analysis_plugin import AbstractAnalysisPlugin
from reporting.analysis_results import FullReport, AnalysisReport

class AnalysisPluginCollection(object):

    def __init__(self, run_arguments):
        self.run_arguments = run_arguments
        self.load_plugins()


    def load_plugins(self):
        self.plugins = []
        self.seen_paths = []
        print(f'Searching plugins in {self.run_arguments.analysis_plugin_directory}')
        self._walk_package(self.run_arguments.analysis_plugin_directory)

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
                    if issubclass(c, AbstractAnalysisPlugin) & (c is not AbstractAnalysisPlugin):
                        print(f'    Found plugin: {c.__module__}.{c.__name__}')
                        self.plugins.append(c())

    def apply_all_plugins_on(self, argument):
        """Apply all of the plugins on the argument supplied to this function
        """
        full_report = FullReport(run_arguments=self.run_arguments)

        for plugin in self.plugins:
            print(f'    Applying {plugin.metadata.name}')
            report = plugin.do_analysis(argument)
            full_report.append_report(report)
        return full_report
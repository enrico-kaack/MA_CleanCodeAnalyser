import pkgutil
import inspect
from AbstractAnalysisPlugin import AbstractAnalysisPlugin

class AnalysisPluginCollection(object):

    def __init__(self, plugin_package):
        self.plugin_package = plugin_package
        self.reload_plugins()


    def reload_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        self.plugins = []
        self.seen_paths = []
        print()
        print(f'Searching plugins in {self.plugin_package}')
        self.walk_package(self.plugin_package)

    def walk_package(self, package):
        """Recursively walk the supplied package to retrieve all plugins
        """
        imported_package = __import__(package, fromlist=[''])

        for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not ispkg:
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
        for plugin in self.plugins:
            print(f'    Applying {plugin.name}')
            plugin.doAnalysis(argument)

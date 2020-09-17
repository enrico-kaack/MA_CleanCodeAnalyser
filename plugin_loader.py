import pkgutil
import inspect
import logging

def load_plugins(plugin_type, directory):
    """Walk the package and get all plugins. 
    """
    logging.debug(f'Searching plugins of type {plugin_type} in {directory}')
    plugins = []
    imported_package = __import__(directory, fromlist=[''])

    for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
        if not ispkg:
            logging.debug(f"importing pluginname  {pluginname}")
            plugin_module = __import__(pluginname, fromlist=[''])
            clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
            for (_, c) in clsmembers:
                # Only add classes that are a sub class of Plugin, but NOT Plugin itself
                if issubclass(c, plugin_type) & (c is not plugin_type):
                    logging.debug(f'    Found plugin: {c.__module__}.{c.__name__}')
                    plugins.append(c())
    return plugins

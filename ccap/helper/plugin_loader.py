import pkgutil
import inspect
import logging
from typing import TypeVar, List, Type
import importlib
import sys
import os

def load_plugins_with_symlinking(plugin_type: Type[object], own_directory: str, custom_directory) -> List[Type[object]]:
    plugins = []
    symlinked_files = _symlink_custom_files(own_directory=own_directory, custom_directory=custom_directory)
    plugins = _load_plugins(plugin_type, directory=own_directory)
    _unlink_files(symlinked_files)
    return plugins

def _symlink_custom_files(own_directory: str, custom_directory: str):
    if custom_directory is None:
        return []

    symlink_files = []
    own_plugin_dir_path = os.path.dirname(importlib.util.find_spec(own_directory).origin)

    for root, dirs, files in os.walk(custom_directory, topdown=False):
        for name in files:
            if os.path.splitext(name)[1] == ".py":
                plugin_path = os.path.join(root, name)
                symlink_path = os.path.join(own_plugin_dir_path, name)
                logging.debug(f"symlinking from {os.path.join(root, name)} to {symlink_path}")
                os.symlink(plugin_path, symlink_path)
                symlink_files.append(symlink_path)
    return symlink_files

def _unlink_files(files: Type[str]):
    for f in files:
        logging.debug(f"unlinking {f}")
        os.unlink(f)

def _load_plugins(plugin_type: Type[object], directory: str) -> List[Type[object]]:
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

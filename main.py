import argparse
import os
from AnalysisPluginCollection import AnalysisPluginCollection


class InputArguments:
    INPUT_DIR = "inputDir"
    ANALYSIS_PLUGIN_DIR = "analysisPluginDir"

    @property
    def input_directory(self):
        return self._inputDirectory
    
    @input_directory.setter
    def input_directory(self, value):
        #TODO: check if it is a correct path
        if os.path.isdir(value):
            self._inputDirectory = os.path.abspath(value)
        else:
            raise FileNotFoundError("Input Directory is not a directory")

    @property
    def analysis_plugin_directory(self):
        return self._analysis_plugin_directory
    
    @analysis_plugin_directory.setter
    def analysis_plugin_directory(self, value):
        #TODO: check if it is a correct path
        if os.path.isdir(value):
            self._analysis_plugin_directory = value
        else:
            raise FileNotFoundError("Analysis Plugin Directory is not a directory")

    def __init__(self):
        self.__parseInputArguments()
    
    def __parseInputArguments(self):
        ap = argparse.ArgumentParser()
        ap.add_argument(self.INPUT_DIR, metavar="<input directory>", type=str, nargs=1, 
            help="Directory Path to be scanned for Python Source Files")
        ap.add_argument("--" + self.ANALYSIS_PLUGIN_DIR, metavar="<analysis plugin directory>",
            help="Directory Path to be scanned for Analysis Plugins")

        args = vars(ap.parse_args())

        print("INPUT ARGS: ", args)

        self.input_directory = args[self.INPUT_DIR][0]
        self.analysis_plugin_directory = args[self.ANALYSIS_PLUGIN_DIR] if args[self.ANALYSIS_PLUGIN_DIR] is not None else "analysis_plugins"



if __name__ == "__main__":
    args = InputArguments()
    my_plugins = AnalysisPluginCollection(args)
    my_plugins.apply_all_plugins_on("Testvalue")
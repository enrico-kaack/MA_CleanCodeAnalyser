import argparse
import os
from AnalysisPluginCollection import AnalysisPluginCollection


class InputArguments:
    INPUT_DIR = "inputDir"

    @property
    def inputDirectory(self):
        return self._inputDirectory
    
    @inputDirectory.setter
    def inputDirectory(self, value):
        #TODO: check if it is a correct path
        if os.path.isdir(value):
            self._inputDirectory = os.path.abspath(value)
        else:
            raise FileNotFoundError("Input Dir is not a directory")

    def __init__(self):
        self.__parseInputArguments()
    
    def __parseInputArguments(self):
        ap = argparse.ArgumentParser()
        ap.add_argument(self.INPUT_DIR, metavar="<input directory>", type=str, nargs=1, 
            help="Directory Path to be scanned for Python Source Files")
        args = vars(ap.parse_args())

        print("INPUT ARGS: ", args)

        self.inputDirectory = args[self.INPUT_DIR][0]



if __name__ == "__main__":
    args = InputArguments()
    my_plugins = AnalysisPluginCollection('analysis_plugins')
    my_plugins.apply_all_plugins_on("Testvalue")
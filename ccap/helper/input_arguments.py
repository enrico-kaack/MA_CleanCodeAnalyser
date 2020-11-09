import argparse
import os
import logging

class Arguments:
    INPUT_DIR = "inputDir"
    ANALYSIS_PLUGIN_DIR = "analysisPluginDir"
    OUTPUT_PLUGIN_DIR = "outputPluginDir"
    OUTPUT = "output"
    VERBOSE = "v"

    @property
    def input_directory(self):
        return self._inputDirectory

    @input_directory.setter
    def input_directory(self, value):
        # TODO: check if it is a correct path
        if os.path.isdir(value):
            self._inputDirectory = os.path.abspath(value)
        else:
            raise FileNotFoundError("Input Directory is not a directory")

    @property
    def analysis_plugin_directory(self):
        return self._analysis_plugin_directory

    @analysis_plugin_directory.setter
    def analysis_plugin_directory(self, value):
        # TODO: check if it is a correct path
        #if os.path.isdir(value):
        self._analysis_plugin_directory = value
        #else:
        #    raise FileNotFoundError("Analysis Plugin Directory is not a directory")

    @property
    def output_plugin_directory(self):
        return self._output_plugin_directory

    @output_plugin_directory.setter
    def output_plugin_directory(self, value):
        #TODO: check if it is a correct path
        #if os.path.isdir(value):
        self._output_plugin_directory = value
        #else:
        #    raise FileNotFoundError("Output Plugin Directory is not a directory")

    def __init__(self):
        self._parseInputArguments()
    
    def _parseInputArguments(self):
        ap = argparse.ArgumentParser()
        ap.add_argument(self.INPUT_DIR, metavar="<input directory>", type=str, nargs=1,
            help="Directory Path to be scanned for Python Source Files")
        ap.add_argument("--" + self.ANALYSIS_PLUGIN_DIR, metavar="<analysis plugin directory>",
            help="Directory Path to be scanned for Analysis Plugins")
        ap.add_argument("--" + self.OUTPUT_PLUGIN_DIR, metavar="<output plugin directory>",
            help="Directory Path to be scanned for Output Plugins")
        ap.add_argument("--" + self.OUTPUT, metavar="<output format plugin>",
            help="Ouput Plugin to use")
        ap.add_argument("-" + self.VERBOSE, action='store_true',
            help="Enable verbose printing")

        args = vars(ap.parse_args())



        self.input_directory = args[self.INPUT_DIR][0]
        self.analysis_plugin_directory = args[self.ANALYSIS_PLUGIN_DIR] if args[self.ANALYSIS_PLUGIN_DIR] is not None else "ccap.analysis_plugins"
        self.output_plugin_directory = args[self.OUTPUT_PLUGIN_DIR] if args[self.OUTPUT_PLUGIN_DIR] is not None else "ccap.output_plugins"
        self.output = args[self.OUTPUT] if args[self.OUTPUT] is not None else "std"
        self.verbose = args[self.VERBOSE] if args[self.VERBOSE] else False

        log_level = logging.DEBUG if self.verbose else logging.ERROR
        logging.basicConfig(level=log_level)
        logging.debug("INPUT ARGS: ", args)


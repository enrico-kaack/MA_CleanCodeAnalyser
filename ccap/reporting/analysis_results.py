from abc import ABC, abstractmethod
from typing import List, Optional
from ccap.plugin_definition.plugin_meta_data import PluginMetaData

class AbstractAnalysisProblem(ABC):

    def __init__(self):
        self.name = "ABSTRACT PROBLEM"
        self.description = "ABSTRACT DESCRIPTION"
        self.file_path = "ABSTRACT FILEPATH"
        self.line_number = None

    def __init__(self, file_path, line_number):
        self.file_path = file_path
        self.line_number = line_number


class AnalysisReport:

    def __init__(self, plugin_metadata: PluginMetaData):
        self.plugin_metadata = plugin_metadata
        self._problems: List[AbstractAnalysisProblem]  = []
    
    @property
    def problems(self):
        return self._problems

    @problems.setter
    def __problems(self, value):
        self._problems = value

    def append_problem(self, problem):
        self.problems.append(problem)


class FullReport:
    analysis_time: Optional[float] = None
    reports: List[AnalysisReport] = []
    def __init__(self, run_arguments):
        self.run_arguments = run_arguments


    def append_report(self, report: AnalysisReport):
        self.reports.append(report)

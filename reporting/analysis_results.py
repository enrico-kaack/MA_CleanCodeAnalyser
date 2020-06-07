from typing import List

class AbstractAnalysisProblem(object):

    def __init__(self):
        self.name = "ABSTRACT PROBLEM"
        self.description ="ABSTRACT DESCRIPTION"
        self.file_path = "ABSTRACT FILEPATH"
        self.line_number = None

    def __init__(self, file_path, line_number):
        self.file_path = file_path
        self.line_number = line_number


class AnalysisReport(object):

    def __init__(self, plugin_metadata):
        self.plugin_metadata = plugin_metadata
        self._problems = []
    
    @property
    def problems(self):
        return self._problems

    @problems.setter
    def __problems(self, value):
        self._problems = value

    def append_problem(self, problem):
        self.problems.append(problem)

class FullReport(object):
    def __init__(self, run_arguments):
        self.run_arguments = run_arguments
        self.analysis_time = None
        self.reports = []

    def append_report(self, report):
        self.reports.append(report)

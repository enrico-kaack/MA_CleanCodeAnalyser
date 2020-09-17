from typing import List, Optional
from ast_parser import ParsedSourceFile
from reporting.analysis_results import AnalysisReport
from abc import ABC, abstractmethod
from plugin_definition.plugin_meta_data import PluginMetaData


class AbstractAnalysisPlugin(ABC):
    metadata: Optional[PluginMetaData] = None

    def __init__(self):
        self.metadata = None

    @abstractmethod
    def do_analysis(self, source_files: List[ParsedSourceFile]) -> AnalysisReport:
        pass

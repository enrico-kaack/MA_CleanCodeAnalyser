from typing import List, Optional
from ccap.components.input_component import ParsedSourceFile
from ccap.reporting.analysis_results import AnalysisReport
from abc import ABC, abstractmethod
from ccap.plugin_definition.plugin_meta_data import PluginMetaData


class AbstractAnalysisPlugin(ABC):
    metadata: PluginMetaData

    def __init__(self):
        self.metadata = None

    @abstractmethod
    def do_analysis(self, source_files: List[ParsedSourceFile]) -> AnalysisReport:
        pass

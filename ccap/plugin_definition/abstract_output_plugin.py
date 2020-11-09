from abc import ABC, abstractmethod
from ccap.reporting.analysis_results import FullReport
from ccap.plugin_definition.plugin_meta_data import PluginMetaData
from typing import Optional

class AbstractOutputPlugin(ABC):
    metadata: Optional[PluginMetaData] = None
    output_format: str = "std"

    def __init__(self):
        pass

    @abstractmethod
    def handle_report(self, full_report: FullReport) -> None:
        raise NotImplementedError

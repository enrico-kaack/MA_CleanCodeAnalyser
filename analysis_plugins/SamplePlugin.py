from AbstractAnalysisPlugin import AbstractAnalysisPlugin

class SamplePlugin(AbstractAnalysisPlugin):
    def __init__(self):
        super().__init__()

        self.name = "Sample Plugin"

    def doAnalysis(self, ast):
        print("Doing work", self.name)
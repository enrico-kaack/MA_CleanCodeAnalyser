
class AbstractAnalysisPlugin(object):
    def __init__(self):
        self.name = "NOT_IMPLEMENTED"
    
    def doAnalysis(self, ast):
        raise NotImplementedError

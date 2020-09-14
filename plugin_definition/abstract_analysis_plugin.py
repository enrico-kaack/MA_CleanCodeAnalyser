
class AbstractAnalysisPlugin(object):
    def __init__(self):
        self.metadata = None

    def do_analysis(self, ast):
        raise NotImplementedError

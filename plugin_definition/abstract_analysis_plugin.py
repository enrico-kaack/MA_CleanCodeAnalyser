
class AbstractAnalysisPlugin(object):
    def __init__(self):
        self.metadata = None

    def do_analysis(self, source_files):
        raise NotImplementedError


class AbstractOutputPlugin(object):
    def __init__(self):
        self.metadata = None
    
    def write_report(self, full_report):
        raise NotImplementedError

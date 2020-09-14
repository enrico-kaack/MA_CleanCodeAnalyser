
class AbstractOutputPlugin(object):
    def __init__(self):
        self.metadata = None
        self.output_format = None
    
    def handle_report(self, full_report):
        raise NotImplementedError

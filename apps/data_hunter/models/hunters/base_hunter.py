

class HunterAbstract(object):
    """
    Parser for multiple source. Content for each source is differnet
    """
    site = ''
    type = ''

    def __init__(self):
        raise NotImplementedError("Constructor Not Implemented")

    def get_content(self):
        content = self.request_content()
        return self.parse_content(content)

    def request_content(self):
        raise NotImplementedError("Request Not Implemented")

    def parse_content(self):
        raise NotImplementedError("Parser Not Implemented")
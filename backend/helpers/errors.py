class HTTPError(Exception):
    def __init__(self, code=500, message="Unspecified server error."):
        self.code = code
        self.message = message


class ParameterError(Exception):
    def __init__(self, code=400, message="Invalid parameters."):
        self.code = code
        self.message = message

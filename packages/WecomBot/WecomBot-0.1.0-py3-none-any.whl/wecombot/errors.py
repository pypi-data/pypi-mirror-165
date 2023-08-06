class RequestError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message

    def __str__(self):
        return f'{self.message} (code={self.code})'


class InvalidKeyError(RequestError):
    """
    Raised on key Invalid.
    """
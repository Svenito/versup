__version__ = "1.3.0"


class VersupError(Exception):
    def __init__(self, message):
        # Call Exception.__init__(message)
        # to use the same Message header as the parent class
        super().__init__(message)

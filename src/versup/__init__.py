__version__ = "1.6.1"


class VersupError(Exception):
    def __init__(self, message: str) -> None:
        # Call Exception.__init__(message)
        # to use the same Message header as the parent class
        super().__init__(message)

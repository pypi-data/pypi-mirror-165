class PloupyException(Exception):
    """
    Base exception for all ploupy-defined exceptions
    """


class InvalidStateException(PloupyException):
    """
    Exception raised when a state is invalid
    """


class InvalidBotKeyException(PloupyException):
    """
    Exception raised when the bot key is invalid
    """


class InvalidServerDataFormatException(PloupyException):
    """
    Exception raised when data received from the server isn't
    in the excepted format
    """


class ActionFailedException(PloupyException):
    """
    Exception raised when an action is refuted by the server
    """

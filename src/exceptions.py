from click import ClickException


class ConfigException(ClickException):
    """An exception that raises when an error occur in credentials config"""

    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message


class SecurityException(ClickException):
    """An exception that raises when an error occur related to security"""

    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message


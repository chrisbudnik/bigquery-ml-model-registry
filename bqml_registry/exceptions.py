class RegistryError(Exception):
    """Base class for registry-related exceptions"""
    pass

class BigQueryPermissionError(RegistryError):
    """Exception raised for permission-related errors."""

    def __init__(self, message="Setup error occurred"):
        self.message = message
        super().__init__(self.message)

class SQLNotFoundError(RegistryError):
    """Exception raised for model sql not found errors."""

    def __init__(self, message="Model not found"):
        self.message = message
        super().__init__(self.message)


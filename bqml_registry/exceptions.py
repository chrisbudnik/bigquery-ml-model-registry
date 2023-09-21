class RegistryError(Exception):
    """Base class for registry-related exceptions"""
    pass

class PermissionsError(RegistryError):
    """Exception raised for permission-related errors."""

    def __init__(self, message="Setup error occurred"):
        self.message = message
        super().__init__(self.message)



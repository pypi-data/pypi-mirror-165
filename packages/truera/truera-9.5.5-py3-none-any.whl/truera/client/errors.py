class UsageException(Exception):
    """Raised when the indicated error is correctable by the user"""


class MissingProject(UsageException):
    """Project was not specified"""


class MissingProjectPath(UsageException):
    """project path was not specified"""


class IncorrectModelSpecification(UsageException):
    """Bad Model specification"""


class FileNotFound(UsageException):
    """a file or path was not found"""


class ModelNotFound(UsageException):
    """model was not found at the path specified"""


class AILensHomeError(UsageException):
    """env ${AILENS_HOME} not set"""


class FileNotCSVError(UsageException):
    """file name was not a CSV file"""


class InsufficientCSVColumns(UsageException):
    """CSV file does not have enough columns"""


class InvalidVersion(Exception):
    """Raised if a Version of a ML Model is incorrect"""


class InvalidSegmentation(Exception):
    """Raised when a constructed Segmentation is invalid"""


class AuthorizationDenied(Exception):
    """Passed through from the RBAC service."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class NotFoundError(Exception):

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class FileDoesNotExistException(Exception):

    def __init__(self, message):
        self.message = message


class MetadataNotFoundException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class DirectoryAlreadyExistsException(Exception):

    def __init__(self, message):
        self.message = message


class InvalidFrameworkWrapperException(Exception):

    def __init__(self, message):
        self.message = message


class MissingEnvironmentSpecException(Exception):

    def __init__(self, message):
        self.message = message


class PackageVerificationException(Exception):

    def __init__(self, message):
        self.message = message
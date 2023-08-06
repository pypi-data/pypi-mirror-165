class DataError(Exception):
    """Base class for data Error"""


class FileError(DataError):
    """Base class for file Error"""


class FileMoveError(FileError):
    """Move file error"""


class NotAFileError(FileError):
    """When it's not a file"""


class DirError(DataError):
    """Base class for folder error"""


class DirMoveError(DirError):
    """Move folder error"""


class DirMoveInsideItselfError(DirMoveError):
    """When try move folder inside itself"""


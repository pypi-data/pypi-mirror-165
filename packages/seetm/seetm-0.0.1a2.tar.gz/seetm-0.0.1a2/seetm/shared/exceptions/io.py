from seetm.shared.exceptions.base import SEETMException


class SEETMIOException(SEETMException):
    pass


class InvalidInitDirException(SEETMIOException):
    pass


class ProjectExistsException(SEETMIOException):
    pass


class YAMLFormatException(SEETMIOException):
    pass


class YAMLFileWriteException(SEETMIOException):
    pass


class NLUFileNotFoundException(SEETMIOException):
    pass


class EvalFileNotFoundException(SEETMIOException):
    pass


class InvalidFileExtensionException(SEETMIOException):
    pass


class InvalidNLUDatasetException(SEETMIOException):
    pass


class EmptyNLUDatasetException(SEETMIOException):
    pass


class InvalidPathSpecifiedException(SEETMIOException):
    pass


class ModelNotFoundException(SEETMIOException):
    pass


class ModelLoadException(SEETMIOException):
    pass


class FileSizeInspectingException(SEETMIOException):
    pass


class InvalidEvalDatasetException(SEETMIOException):
    pass


class EmptyEvalDatasetException(SEETMIOException):
    pass


class ConfigFileNotFoundException(SEETMIOException):
    pass

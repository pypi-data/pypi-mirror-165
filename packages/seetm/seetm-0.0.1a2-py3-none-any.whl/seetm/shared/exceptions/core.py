from seetm.shared.exceptions.base import SEETMException


class SEETMCoreException(SEETMException):
    pass


class MapperException(SEETMCoreException):
    pass


class InvalidDataInstanceException(SEETMCoreException):
    pass


class InvalidNumberOfTokensException(SEETMCoreException):
    pass


class MapLoadingException(SEETMCoreException):
    pass


class ExportableInitializationException(SEETMCoreException):
    pass


class ExportablePersistException(SEETMCoreException):
    pass


class EvaluationPersistException(SEETMCoreException):
    pass


class EvaluationDatasetExportException(SEETMCoreException):
    pass


class MappingExportException(SEETMCoreException):
    pass


class InvalidEvaluationLevelException(SEETMCoreException):
    pass


class InvalidEvaluationMethodException(SEETMCoreException):
    pass


class InvalidMappingMethodException(SEETMCoreException):
    pass


class Word2VecModelTrainingException(SEETMCoreException):
    pass


class Word2VecModelNotFoundException(SEETMCoreException):
    pass


class ZeroMappedTokensException(SEETMCoreException):
    pass


class ZeroExtractableTokensException(SEETMCoreException):
    pass


class ZeroValidTokensException(SEETMCoreException):
    pass


class OutDatedEvaluationDatasetException(SEETMCoreException):
    pass


class ExtractorCleanupException(SEETMCoreException):
    pass

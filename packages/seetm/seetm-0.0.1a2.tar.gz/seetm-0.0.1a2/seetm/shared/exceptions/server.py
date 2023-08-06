from seetm.shared.exceptions.base import SEETMException


class SEETMServerException(SEETMException):
    pass


class ServerNotFoundException(SEETMServerException):
    pass


class ProcessTerminationException(SEETMServerException):
    pass


class InvalidProcessIDException(SEETMServerException):
    pass


class ProcessQueueException(SEETMServerException):
    pass


class ProcessQueuePushException(SEETMServerException):
    pass


class ProcessQueueUpdateException(SEETMServerException):
    pass


class ProcessQueuePullException(SEETMServerException):
    pass


class ProcessAlreadyExistsException(SEETMServerException):
    pass


class ProcessNotExistsException(SEETMServerException):
    pass


class MetadataRetrievalException(SEETMServerException):
    pass


class InvalidRequestIDException(SEETMServerException):
    pass


class ServerCacheException(SEETMServerException):
    pass


class ServerCachePushException(SEETMServerException):
    pass


class ServerCachePullException(SEETMServerException):
    pass


class ModelNotFoundException(SEETMServerException):
    pass


class ExplanationNotFoundException(SEETMServerException):
    pass


class InvalidExplanationSpecifiedException(SEETMServerException):
    pass


class InvalidServerConfigsException(SEETMServerException):
    pass


class ServerConfigsPersistException(SEETMServerException):
    pass


class InvalidConfigurationTypeSpecifiedException(SEETMServerException):
    pass


class CustomConfigsNotFoundException(SEETMServerException):
    pass

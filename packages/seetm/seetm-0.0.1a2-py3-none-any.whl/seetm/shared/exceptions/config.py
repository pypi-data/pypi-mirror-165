from seetm.shared.exceptions.base import SEETMException


class SEETMConfigException(SEETMException):
    pass


class InvalidInterfaceException(SEETMConfigException):
    pass


class InvalidConfigKeyException(SEETMConfigException):
    pass

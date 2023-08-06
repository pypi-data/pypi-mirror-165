# SEETM
PACKAGE_NAME = "seetm"
PACKAGE_NAME_PYPI = "seetm"
PACKAGE_VERSION = "0.0.1a2"
PACKAGE_VERSION_LONG = f'SEETM Version: {PACKAGE_VERSION}'
LANGUAGES_SUPPORTED = ['en', 'si']


class InterfaceType:
    CLI = "cli"
    INIT = "init"
    SERVER = "server"
    MAPPER = "map"
    EVALUATOR = "evaluate"
    EXTRACTOR = "extract"
    NONE = ""


class LoggingLevel:
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    QUIET = 60


class Validity:
    VALID = "valid"
    INVALID = "invalid"
    NOTSET = "n/a"


# SERVER
DEFAULT_PORT = 6067
DEFAULT_HOST_DEC = "0.0.0.0"
DEFAULT_HOST_LOCAL = "localhost"
SEETM_ASCII_LOGO = """
█▀ █▀▀ █▀▀ ▀█▀ █▀▄▀█
▄█ ██▄ ██▄ ░█░ █░▀░█
"""
SEETM_ASCII_LOGO_V2 = """
丂㠪㠪ㄒ爪
"""


class ServerEnv:
    STRICT_LOCAL = "strict_local"  # triggers server explanations without subprocess
    DEV = "dev"  # enables server debugging
    PROD = "prod"  # disables server debugging


class ServerConfigType:
    JSON = "json"
    NONE = "none"


# MAPPER
class MappingMethod:
    IPA = "ipa"
    RULE_BASED = "rule-based"
    TRANSLATE = "translate"


class MapperType:
    JSON = "json"
    DICT = "dict"
    QUIET = "quiet"


ENGLISH_TOKEN_PATTERN = r"^[a-zA-Z]+$"
EN_TO_PHONETICS_MAP_PATH = "./seetm_maps/en_to_phonetics_map.json"
TOKEN_TO_TOKEN_MAP_PATH = "./seetm_maps/token_to_token_map.json"

# SCAFFOLD
DEFAULT_INIT_SRC_DIR_NAME = "init_dir"
DEFAULT_INIT_CACHE_DIR_NAME = ".seetm_init_"
DEFAULT_INIT_FILES_TO_EXCLUDE = ['__pycache__', '__main__.py']
DEFAULT_INIT_DEST_DIR_NAME = "./"
RASA_DIRS_IN_SEETM_INIT = ["data"]
INVALID_DIR_NAME_CHARS = ['\\', '/', '<', '>', ':', '*', '?', '|']
ALLOWED_INIT_DIR_NAMES = [".", "./", "None", "none"]


class DestinationDirType:
    RASA = "rasa"
    SEETM = "seetm"
    EMPTY = "empty"
    VALID = "valid"
    INVALID = "invalid"


# RASA DATA FILES
DEFAULT_DATA_PATH = "./data"
YAML_EXTENSIONS = [".yaml", ".yml"]
DEFAULT_YAML_VERSION = "2.0"
DEFAULT_NLU_YAML_TAG = "nlu"
DEFAULT_VERSION_YAML_TAG = "version"
DEFAULT_NLU_INTENT_TAG = "intent"
DEFAULT_NLU_EXAMPLES_TAG = "examples"
DEFAULT_NLU_LOCATION_TAG = "location"


# EVAL DATA FILES
DEFAULT_EVALUATION_DATA_PATH = "./seetm_eval/"
DEFAULT_EVALUATION_RESULTS_PATH = "./seetm_eval/results"
DEFAULT_EMBEDDING_MODELS_PATH = "./seetm_eval/word2vec_models"

DEFAULT_EVAL_YAML_TAG = "eval"
DEFAULT_EVAL_TOKEN_TAG = "token"
DEFAULT_EVAL_TEST_TOKEN_TAG = "test_token"
DEFAULT_EVAL_MAPPED_TOKEN_TAG = "mapped_token"


class ExportableType:
    NLU = "nlu"
    EVAL = "eval"


class EvaluationLevel:
    TOKEN = "token"
    VECTOR = "vector"


# FILE IO
class FilePermission:
    READ = "r"
    WRITE = "w"


class Encoding:
    UTF8 = "utf8"


# TERMINAL
class TermColor:
    # source:
    # https://pkg.go.dev/github.com/whitedevops/colors

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END_C = "\033[0m"
    NONE_C = ""

    DEFAULT = "\033[39m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    LIGHTGRAY = "\033[37m"
    DARKGRAY = "\033[90m"
    LIGHTRED = "\033[91m"
    LIGHTGREEN = "\033[92m"
    LIGHTYELLOW = "\033[93m"
    LIGHTBLUE = "\033[94m"
    LIGHTMAGENTA = "\033[95m"
    LIGHTCYAN = "\033[96m"
    WHITE = "\033[97m"

    BDEFAULT = "\033[49m"
    BBLACK = "\033[40m"
    BRED = "\033[41m"
    BGREEN = "\033[42m"
    BYELLOW = "\033[43m"
    BBLUE = "\033[44m"
    BMAGENTA = "\033[45m"
    BCYAN = "\033[46m"
    BGRAY = "\033[47m"
    BDARKGRAY = "\033[100m"
    BLIGHTRED = "\033[101m"
    BLIGHTGREEN = "\033[102m"
    BLIGHTYELLOW = "\033[103m"
    BLIGHTBLUE = "\033[104m"
    BLIGHTMAGENTA = "\033[105m"
    BLIGHTCYAN = "\033[106m"
    BWHITE = "\033[107m"


# EVALUATOR
class Metrics:
    SEQUENCE_MATCHING = "sequence-matching"
    EDIT_DISTANCE = "edit-distance"


# CONFIGS
class Config:
    DEFAULT_CONFIG_PATH = "./seetm_config.yml"

    BASE_CONFIGS_KEY = "seetm_base_configs"
    SERVER_CONFIGS_KEY = "seetm_server_configs"

    DATA_PATH_KEY = "data_path"
    METHOD_KEY = "method"
    METRIC_KEY = "metric"
    CASE_SENSITIVE_KEY = "case_sensitive"

    HOST_KEY = "host"
    PORT_KEY = "port"

    VALID_MAIN_KEYS = ["seetm_base_configs", "seetm_server_configs"]
    VALID_BASE_KEYS = ["data_path", "method", "metric", "case_sensitive"]
    VALID_SERVER_KEYS = ["host", "port"]


class ConfigType:
    ALL = "all"
    BASE = "base"
    SERVER = "server"


# EXPORTABLE
DEFAULT_EXPORTABLE_PATH = "./seetm_exports/"
DEFAULT_TOKENIZER_PERSIST_PATH = "./seetm_exports/tokenizer_mappings.json"

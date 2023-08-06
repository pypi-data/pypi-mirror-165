import json
import logging
from typing import Dict, Text

from seetm.shared.constants import (
    InterfaceType,
    Encoding,
    FilePermission,
    Metrics,
    Config,
    DEFAULT_DATA_PATH,
    MappingMethod,
    DEFAULT_PORT,
    DEFAULT_HOST_LOCAL,
    ConfigType,
    DEFAULT_HOST_DEC,
)
from seetm.shared.exceptions.config import (
    InvalidInterfaceException,
    InvalidConfigKeyException,
)
from seetm.utils.io import (
    read_yaml_file,
    dir_exists,
)

logger = logging.getLogger(__name__)


def get_init_configs(
        config_path: Text = None,
        data_path: Text = None,
        instance: Text = None,
        method: Text = None,
        metric: Text = None,
        case: bool = True,
        level: Text = None,
        port: int = None,
        interface: Text = None,
) -> Dict:
    # setting default config file
    # path if not specified
    if not config_path:
        config_path = Config.DEFAULT_CONFIG_PATH

    # interface warnings
    if not interface:
        interface = InterfaceType.NONE

    if interface not in [InterfaceType.MAPPER, InterfaceType.SERVER, InterfaceType.EVALUATOR, InterfaceType.EXTRACTOR]:
        logger.error("An invalid interface has been specified. Valid "
                     "interfaces are MAPPER, SERVER, EVALUATOR, and EXTRACTOR")
        raise InvalidInterfaceException()

    # loading default configs
    try:
        yaml_content = read_yaml_file(
            yaml_file=config_path,
            encoding=Encoding.UTF8,
            mode=FilePermission.READ,
            version_check=False,
        )

        if not yaml_content:
            logger.warning(f"The given config file '{config_path}' is invalid. "
                           f"SEETM will utilize default configs instead")
    except FileNotFoundError:
        yaml_content = None
        logger.warning(f"Could not locate the '{config_path}' file. "
                       f"SEETM will utilize default configs instead")

    yaml_content_json = json.loads(json.dumps(yaml_content, ensure_ascii=False))
    default_configs = get_default_configs(section=ConfigType.ALL)

    if yaml_content_json:
        # validate keys
        invalid_keys = list()
        for key in yaml_content_json.keys():
            if key not in Config.VALID_MAIN_KEYS:
                invalid_keys.append(key)

        if Config.BASE_CONFIGS_KEY in yaml_content_json:
            base_dict = dict()
            for element in yaml_content_json[Config.BASE_CONFIGS_KEY]:
                base_dict = {**base_dict, **element}

            for key in base_dict.keys():
                if key not in Config.VALID_BASE_KEYS:
                    invalid_keys.append(key)

        if Config.SERVER_CONFIGS_KEY in yaml_content_json:
            server_dict = dict()
            for element in yaml_content_json[Config.SERVER_CONFIGS_KEY]:
                server_dict = {**server_dict, **element}

            for key in server_dict.keys():
                if key not in Config.VALID_SERVER_KEYS:
                    invalid_keys.append(key)

        if invalid_keys:
            logger.warning(f"Found Invalid Configuration YAML keys: {', '.join(invalid_keys)}")
            raise InvalidConfigKeyException()

        for main_key in yaml_content_json.keys():
            main_key_dict = dict()
            for element in yaml_content_json[main_key]:
                main_key_dict = {**main_key_dict, **element}

            for sub_key, value in main_key_dict.items():
                if sub_key == Config.DATA_PATH_KEY and not data_path and not instance:
                    if not dir_exists(value) and interface != InterfaceType.EVALUATOR:
                        logger.warning("Data path specified is invalid. SEETM will treat "
                                       f"'{default_configs[Config.BASE_CONFIGS_KEY][Config.DATA_PATH_KEY]}' "
                                       f"as the default data path.")
                        continue
                elif sub_key == Config.METHOD_KEY and not method:
                    if value not in [MappingMethod.IPA, MappingMethod.RULE_BASED] and \
                            interface != InterfaceType.EVALUATOR:
                        logger.warning("Mapping method specified is invalid. SEETM will utilize "
                                       f"'{default_configs[Config.BASE_CONFIGS_KEY][Config.METHOD_KEY]}' "
                                       f"as the default mapping method.")
                        continue
                elif sub_key == Config.METRIC_KEY and not metric:
                    if value not in [Metrics.EDIT_DISTANCE, Metrics.SEQUENCE_MATCHING] and \
                            interface == InterfaceType.EVALUATOR:
                        logger.warning("Metric specified is invalid. SEETM will utilize "
                                       f"'{default_configs[Config.BASE_CONFIGS_KEY][Config.METRIC_KEY]}' "
                                       f"as the default evaluation metric.")
                        continue
                elif sub_key == Config.PORT_KEY and not port:
                    if not isinstance(value, int) and interface == InterfaceType.SERVER:
                        logger.warning("Port specified is either invalid or unavailable. SEETM will utilize "
                                       f"'{default_configs[Config.SERVER_CONFIGS_KEY][Config.PORT_KEY]}' "
                                       f"as the default port to start SEETM server at.")
                        continue
                elif sub_key == Config.HOST_KEY:
                    if value not in [DEFAULT_HOST_LOCAL, DEFAULT_HOST_DEC] and \
                            interface == InterfaceType.SERVER:
                        logger.warning("Host specified is either invalid or unavailable. SEETM will utilize "
                                       f"'{default_configs[Config.SERVER_CONFIGS_KEY][Config.HOST_KEY]}' "
                                       f"as the default host to start SEETM server at.")
                        continue
                default_configs[main_key][sub_key] = value

    if data_path and interface == InterfaceType.EXTRACTOR:
        default_configs[Config.BASE_CONFIGS_KEY][Config.DATA_PATH_KEY] = data_path
        logger.warning("Data path specified in the config file will be ignored "
                       "since --data-path argument was set via the CLI")
    if instance and interface != InterfaceType.EVALUATOR:
        default_configs[Config.BASE_CONFIGS_KEY][Config.DATA_PATH_KEY] = [instance]
        logger.warning("Data path specified in the config file will be ignored "
                       "since --instance argument was set via the CLI")
    if method:
        if method in [MappingMethod.IPA, MappingMethod.RULE_BASED, MappingMethod.TRANSLATE]:
            default_configs[Config.BASE_CONFIGS_KEY][Config.METHOD_KEY] = method
            logger.warning("Mapping method specified in the config file will be ignored "
                           "since --method argument was set via the CLI")
    if port and interface == InterfaceType.SERVER:
        if isinstance(port, int):
            default_configs[Config.SERVER_CONFIGS_KEY][Config.PORT_KEY] = port
            logger.warning("Port specified in the config file will be ignored "
                           "since --port argument was set via the CLI")
    if isinstance(case, bool) and case is False:
        default_configs[Config.BASE_CONFIGS_KEY][Config.CASE_SENSITIVE_KEY] = case
        logger.warning("Case sensitivity specified in the config file will be ignored "
                       "since --no-case argument was set via the CLI")
    if interface == InterfaceType.EVALUATOR:
        if metric in [Metrics.EDIT_DISTANCE, Metrics.SEQUENCE_MATCHING]:
            default_configs[Config.BASE_CONFIGS_KEY][Config.METRIC_KEY] = metric
            logger.warning("Evaluation metric specified in the config file will be ignored "
                           "since --metric argument was set via the CLI")

    return default_configs


def get_default_configs(section: Text = ConfigType.ALL) -> Dict:
    default_configs = {
        "seetm_base_configs": {
            "data_path": DEFAULT_DATA_PATH,
            "method": MappingMethod.RULE_BASED,
            "metric": Metrics.EDIT_DISTANCE,
            "case_sensitive": True,
        },
        "seetm_server_configs": {
            "host": DEFAULT_HOST_LOCAL,
            "port": DEFAULT_PORT,
        }
    }

    if section == ConfigType.BASE:
        return default_configs[Config.BASE_CONFIGS_KEY]
    elif section == ConfigType.SERVER:
        return default_configs[Config.SERVER_CONFIGS_KEY]
    else:
        return default_configs

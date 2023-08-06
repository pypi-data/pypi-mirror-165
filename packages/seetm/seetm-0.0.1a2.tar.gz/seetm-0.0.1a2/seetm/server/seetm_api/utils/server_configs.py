import json
import logging
import os
from typing import Dict, NoReturn, Tuple, Text

import ruamel.yaml as yml

from seetm.shared.constants import (
    Config,
    Validity,
    ServerConfigType,
    Encoding,
    FilePermission,
)
from seetm.shared.exceptions.config import (
    SEETMConfigException,
)
from seetm.shared.exceptions.io import (
    ConfigFileNotFoundException,
)
from seetm.shared.exceptions.server import (
    InvalidServerConfigsException,
    ServerConfigsPersistException,
    InvalidConfigurationTypeSpecifiedException,
    CustomConfigsNotFoundException,
)
from seetm.utils.io import (
    nlu_data_dir_exists,
)
from seetm.utils.io import read_yaml_file

logger = logging.getLogger(__name__)


class ServerConfigs:
    def __init__(self):
        self.configs_yml = None
        try:
            self._initialize()
        except Exception as e:
            logger.error(f"Exception occurred while initializing server configs. {e}")
            raise InvalidServerConfigsException(e)

    def _initialize(self) -> NoReturn:
        try:
            yaml_content = read_yaml_file(
                yaml_file=Config.DEFAULT_CONFIG_PATH,
                version_check=False,
            )
            self.configs_yml = yaml_content
            self.configs = json.loads(json.dumps(yaml_content, ensure_ascii=False))
            for key in self.configs.keys():
                key_content_dict = dict()
                for element_dict in self.configs[key]:
                    for element_key, element_value in element_dict.items():
                        key_content_dict[element_key] = element_value

                self.configs[key] = key_content_dict
        except FileNotFoundError:
            raise ConfigFileNotFoundException("Could not locate the 'seetm_config.yml' file. "
                                              "Make sure it is in the root directory")
        except Exception as e:
            logger.error(f"Exception occurred while retrieving 'seetm_config.yml'. {e}")
            raise SEETMConfigException(e)

    @staticmethod
    def validate(configs: Dict) -> Tuple[bool, Dict]:
        validate_status_obj = {
            "keys": Validity.NOTSET,
            Config.DATA_PATH_KEY: Validity.NOTSET,
        }
        validate_status = False

        try:
            keys = list(configs)
            if sorted(keys) != sorted([Config.DATA_PATH_KEY]):
                logger.error("Failed to validate updated server config keys")
                validate_status_obj['keys'] = Validity.INVALID
            else:
                validate_status_obj['keys'] = Validity.VALID

            # data path validation
            if not nlu_data_dir_exists(dir_path=configs[Config.DATA_PATH_KEY]):
                logger.error("Failed to validate data path in updated server configs")
                validate_status_obj[Config.DATA_PATH_KEY] = Validity.INVALID
            else:
                validate_status_obj[Config.DATA_PATH_KEY] = Validity.VALID

            # check if all keys are valid
            if Validity.INVALID in validate_status_obj.values():
                validate_status = False
            else:
                validate_status = True
            return validate_status, validate_status_obj
        except Exception as e:
            logger.error(f"Exception occurred while validating server configurations. {e}")
            return validate_status, validate_status_obj

    def update_and_persist(self, updated_configs: Dict, validate: bool = True):
        try:
            # latest configs
            self._initialize()
            
            if validate:
                if not self.validate(updated_configs)[0]:
                    raise InvalidServerConfigsException()

            seetm_base_configs = self.configs_yml.get(Config.BASE_CONFIGS_KEY)
            for k, v in updated_configs.items():
                for index, element in enumerate(seetm_base_configs):
                    if k in dict(element).keys():
                        seetm_base_configs[index] = {k: v}
            self.configs_yml[Config.BASE_CONFIGS_KEY] = seetm_base_configs

            # modifying the latest configs
            with open(
                    file=os.path.join(Config.DEFAULT_CONFIG_PATH),
                    encoding=Encoding.UTF8,
                    mode=FilePermission.WRITE
            ) as server_configs:
                yaml = yml.YAML()
                yaml.indent(sequence=4, offset=2)
                yaml.dump(self.configs_yml, server_configs)

            # retrieve saved configs
            self._initialize()

            logger.debug("Saved server configs")
        except Exception as e:
            raise ServerConfigsPersistException(e)

    def retrieve(self, config_type: Text = ServerConfigType.JSON, custom_configs: bool = False) -> Text:
        if not config_type or config_type not in [ServerConfigType.JSON, ServerConfigType.NONE]:
            raise InvalidConfigurationTypeSpecifiedException()

        if custom_configs:
            try:
                sinhala = bool(os.environ.get("SINHALA_ENABLED"))
                app_env = os.environ.get("APP_ENV")
                app_theme = os.environ.get("APP_THEME")
                self.configs["custom_configs"] = {
                    "sinhala_enabled": sinhala,
                    "app_theme": app_theme,
                    "app_env": app_env,
                }
            except Exception as e:
                logger.error("Failed to retrieve custom server configs.")
                raise CustomConfigsNotFoundException(e)

        if config_type == ServerConfigType.JSON:
            return json.dumps(self.configs, indent=4, ensure_ascii=False).encode(Encoding.UTF8).decode()
        else:
            return self.configs

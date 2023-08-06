import logging
from typing import NoReturn, Dict, Text

from seetm.core.token_mapper import TokenMapper
from seetm.shared.constants import (
    MappingMethod,
    Config,
    DEFAULT_NLU_EXAMPLES_TAG,
    DEFAULT_NLU_LOCATION_TAG,
)
from seetm.shared.exceptions.base import SEETMException
from seetm.shared.exceptions.core import (
    SEETMCoreException,
    MapperException,
    InvalidDataInstanceException,
    ExportableInitializationException,
)
from seetm.shared.exceptions.io import (
    SEETMIOException,
    EmptyNLUDatasetException,
    InvalidFileExtensionException,
    InvalidNLUDatasetException,
    NLUFileNotFoundException,
    YAMLFormatException,
)
from seetm.shared.exportable import Exportable
from seetm.utils.io import (
    dir_exists,
    get_rasa_testing_data,
)

logger = logging.getLogger(__name__)


class SEETMCLIMapper:
    def __init__(
            self,
            configs: Dict,
            persist: bool = False,
            quiet_mode: bool = False,
    ) -> NoReturn:
        self.data_path = configs[Config.BASE_CONFIGS_KEY][Config.DATA_PATH_KEY]
        self.method = configs[Config.BASE_CONFIGS_KEY][Config.METHOD_KEY]
        self.case_sensitive = configs[Config.BASE_CONFIGS_KEY][Config.CASE_SENSITIVE_KEY]
        self.persist = persist
        self.quiet_mode = quiet_mode
        self.token_mapper = TokenMapper(
            method=self.method,
            case_sensitive=self.case_sensitive,
            quiet_mode=self.quiet_mode,
        )

    def _map(self, instance: Text) -> Text:
        return self.token_mapper.map(data_instance=instance)

    def run(self) -> NoReturn:
        logger.debug("Initializing SEETM CLI Mapper...")

        # Deprecations, Errors and Warnings
        # for SEETM CLI arguments
        if self.method not in [MappingMethod.IPA, MappingMethod.RULE_BASED]:
            logger.error("Methods other than IPA and Rule-based are not yet supported by SEETM.")
            exit()

        if isinstance(self.data_path, str):
            if not dir_exists(self.data_path):
                raise InvalidNLUDatasetException()

            nlu_dataset = get_rasa_testing_data(
                testing_data_dir=self.data_path,
                preserve_location=True,
            )

            if not nlu_dataset:
                EmptyNLUDatasetException()

            mapped_list = list()
            for intent in nlu_dataset.keys():
                nlu_file = nlu_dataset[intent][DEFAULT_NLU_LOCATION_TAG]
                for example in nlu_dataset[intent][DEFAULT_NLU_EXAMPLES_TAG]:
                    mapped_instance = self._map(instance=example)
                    mapped_list.append({
                        "instance": example,
                        "mapped_instance": mapped_instance,
                        "intent": intent,
                        "nlu_file": nlu_file,
                        "method": self.method,
                    })

            exportable = Exportable(exportable=mapped_list)
            if not self.quiet_mode:
                exportable.inspect()
            if self.persist:
                exportable.persist()

        else:
            instance = self.data_path[0]
            mapped_instance = self._map(instance=instance)
            mapped_list = [
                {
                    "instance": instance,
                    "mapped_instance": mapped_instance,
                    "intent": "none",
                    "nlu_file": "none",
                    "method": self.method,
                }
            ]

            exportable = Exportable(exportable=mapped_list)
            if not self.quiet_mode:
                exportable.inspect()
            if self.persist:
                exportable.persist()

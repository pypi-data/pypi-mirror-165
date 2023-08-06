import logging
from typing import List, Optional, Text, NoReturn, Dict

from seetm.shared.exceptions.io import EmptyNLUDatasetException
from seetm.utils.io import (
    get_rasa_testing_data,
    get_unique_list,
)

logger = logging.getLogger(__name__)


class RASANLUData:
    def __init__(
            self,
            data_path: Text = None,
    ):
        self.data_path = data_path
        self._initialize_nlu_data()

    def _initialize_nlu_data(self) -> NoReturn:
        logger.debug(f"Loading data using SEETM Testing data loader...")

        self._testing_data = get_rasa_testing_data(
            testing_data_dir=self.data_path,
            case_sensitive=True,
            preserve_location=True,
        )

        if not self._testing_data:
            raise EmptyNLUDatasetException()

        logger.info(f'Total number of intents: {self.get_intent_size()}')
        logger.info(f'Total number of data instances: {self.get_instance_size()}')

    def get_testing_data(
            self,
    ) -> Dict:
        testing_data = self._testing_data
        return testing_data

    def get_instances(
            self,
            intent: Text = None,
    ) -> Optional[List]:
        all_instances = list()
        if intent:
            if intent in self._testing_data:
                all_instances = self._testing_data[intent]
            else:
                logger.error("Could not find the given intent name in testing "
                             "data. Please input a valid intent name.")
        else:
            for key, value in self._testing_data.items():
                all_instances += value
        return get_unique_list(all_instances)

    def get_instance_size(
            self,
            intent: Text = None,
    ) -> Optional[int]:
        filtered_instances = self.get_instances(intent=intent)
        return len(filtered_instances)

    def get_intents(self) -> Optional[List]:
        if not self._testing_data:
            return []
        intents = list(self._testing_data.keys())
        return intents

    def get_intent_size(self) -> Optional[int]:
        if not self._testing_data:
            return 0
        return len(self._testing_data.keys())

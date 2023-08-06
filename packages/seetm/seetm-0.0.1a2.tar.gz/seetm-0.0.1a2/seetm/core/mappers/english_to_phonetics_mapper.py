import json
import logging
from copy import deepcopy
from typing import Text

from seetm.shared.constants import (
    Encoding,
    FilePermission,
    EN_TO_PHONETICS_MAP_PATH,
)

logger = logging.getLogger(__name__)


class EnglishToPhoneticsMapper:
    def __init__(self):
        try:
            with open(
                    file=EN_TO_PHONETICS_MAP_PATH,
                    mode=FilePermission.READ,
                    encoding=Encoding.UTF8
            ) as en_to_phonetics_map_file:
                self.en_to_phonetics_map = json.load(en_to_phonetics_map_file)
        except Exception as e:
            logger.debug(e)
            logger.warning("Failed to load en_to_phonetics_map.json. External mappings will be ignored")
            self.en_to_phonetics_map = {}

    def map(self, token: Text) -> Text:
        token_copy = str.lower(deepcopy(token))
        if token_copy in self.en_to_phonetics_map:
            mapped_token = self.en_to_phonetics_map[token_copy]
            return mapped_token if mapped_token else token
        else:
            return token


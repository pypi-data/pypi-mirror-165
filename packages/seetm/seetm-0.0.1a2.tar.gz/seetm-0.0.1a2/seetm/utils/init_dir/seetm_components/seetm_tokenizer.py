import json
import logging
from copy import deepcopy
from typing import Any, Dict, List, Text

import rasa.shared.utils.io
import rasa.utils.io
import regex
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.shared.nlu.training_data.message import Message

from seetm.core.token_mapper import TokenMapper
from seetm.shared.constants import (
    MappingMethod,
    Config,
    InterfaceType,
    DEFAULT_TOKENIZER_PERSIST_PATH, FilePermission, Encoding,
)
from seetm.utils.config import get_init_configs

logger = logging.getLogger(__name__)


class SEETMTokenizer(Tokenizer):
    defaults = {
        # Case sensitivity
        "case_sensitive": True,
        # Persisting mappings
        "persist": False
    }

    # the following language should not be tokenized using the WhitespaceTokenizer
    not_supported_language_list = ["zh", "ja", "th"]

    def __init__(self, component_config: Dict[Text, Any] = None) -> None:
        """Construct a new tokenizer using the WhitespaceTokenizer framework."""

        super().__init__(component_config)

        self.emoji_pattern = rasa.utils.io.get_emoji_regex()
        self.case_sensitive = component_config["case_sensitive"] if "case_sensitive" in component_config else True
        self.persist_mapped = component_config["persist"] if "persist" in component_config else False
        self.seetm_configs = get_init_configs(
            config_path=Config.DEFAULT_CONFIG_PATH,
            method=MappingMethod.RULE_BASED,
            interface=InterfaceType.MAPPER,
            case=self.case_sensitive,
        )
        self.token_mapper = TokenMapper(
            method=MappingMethod.RULE_BASED,
            case_sensitive=self.case_sensitive,
            quiet_mode=True
        )

        if self.case_sensitive in self.component_config:
            rasa.shared.utils.io.raise_warning("All English tokens will be lowercased "
                                               "prior to the mapping process")

        if self.persist_mapped:
            rasa.shared.utils.io.raise_warning("Persisting mapped instances may affect "
                                               "the training duration of the model")
            try:
                seetm_tokenizer_mappings = {
                    "mapped_instances": []
                }
                with open(
                        DEFAULT_TOKENIZER_PERSIST_PATH,
                        encoding=Encoding.UTF8,
                        mode=FilePermission.WRITE
                ) as seetm_tokenizer_mappings_file:
                    json.dump(
                        seetm_tokenizer_mappings,
                        seetm_tokenizer_mappings_file,
                        ensure_ascii=False,
                        indent=4
                    )
            except Exception as e:
                logger.error("Error occurred while initializing the mapping persisting source. "
                             "Training will be resumed without persisting maps.")
                logger.debug(e)
                self.persist_mapped = False

    def remove_emoji(self, text: Text) -> Text:
        """Remove emoji if the full text, aka token, matches the emoji regex."""
        match = self.emoji_pattern.fullmatch(text)

        if match is not None:
            return ""

        return text

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = message.get(attribute)
        previous_text = deepcopy(text)

        # SEETM Mapping
        text = self.token_mapper.map(data_instance=text)
        
        # Persisting mapped instances if requested
        try:
            if self.persist_mapped:
                with open(
                        file=DEFAULT_TOKENIZER_PERSIST_PATH,
                        mode=FilePermission.READ,
                        encoding=Encoding.UTF8
                ) as seetm_tokenizer_mappings_file:
                    seetm_tokenizer_mappings = json.load(fp=seetm_tokenizer_mappings_file)

                seetm_tokenizer_mappings["mapped_instances"] = [
                    *seetm_tokenizer_mappings["mapped_instances"],
                    {
                        "instance": previous_text,
                        "mapped_instance": text
                    }
                ]
                with open(
                        DEFAULT_TOKENIZER_PERSIST_PATH,
                        encoding=Encoding.UTF8,
                        mode=FilePermission.WRITE
                ) as seetm_tokenizer_mappings_file:
                    json.dump(
                        seetm_tokenizer_mappings,
                        seetm_tokenizer_mappings_file,
                        ensure_ascii=False,
                        indent=4
                    )
        except Exception as e:
            logger.debug("Error occurred while persisting mapped instances. "
                         f"Training will be resumed without persisting maps. {e}")

        # we need to use regex instead of re, because of
        # https://stackoverflow.com/questions/12746458/python-unicode-regular-expression-matching-failing-with-some-unicode-characters

        # remove 'not a word character' if
        words = regex.sub(
            # there is a space or an end of a string after it
            r"[^\w#@&]+(?=\s|$)|"
            # there is a space or beginning of a string before it
            # not followed by a number
            r"(\s|^)[^\w#@&]+(?=[^0-9\s])|"
            # not in between numbers and not . or @ or & or - or #
            # e.g. 10'000.00 or blabla@gmail.com
            # and not url characters
            r"(?<=[^0-9\s])[^\w._~:/?#\[\]()@!$&*+,;=-]+(?=[^0-9\s])",
            " ",
            text,
        ).split()

        words = [self.remove_emoji(w) for w in words]
        words = [w for w in words if w]

        # if we removed everything like smiles `:)`, use the whole text as 1 token
        if not words:
            words = [text]

        tokens = self._convert_words_to_tokens(words, text)
        return self._apply_token_pattern(tokens)

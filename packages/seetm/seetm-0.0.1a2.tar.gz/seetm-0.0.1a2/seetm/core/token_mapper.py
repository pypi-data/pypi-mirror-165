import logging
from typing import Text, Union, Tuple, List

import eng_to_ipa as ipa
import regex

from seetm.core.mappers.english_to_phonetics_mapper import (
    EnglishToPhoneticsMapper,
)
from seetm.core.mappers.ipa_to_sinhala_mapper import (
    IPAToSinhalaMapper,
)
from seetm.core.mappers.token_to_token_mapper import (
    TokenToTokenMapper,
)
from seetm.shared.constants import (
    MappingMethod,
    ENGLISH_TOKEN_PATTERN,
)
from seetm.shared.exceptions.core import (
    InvalidDataInstanceException,
    MapperException, InvalidMappingMethodException,
)
from seetm.utils.text_preprocessing import tokenize

logger = logging.getLogger(__name__)
EN_PATTERN = regex.compile(ENGLISH_TOKEN_PATTERN)


class TokenMapper:
    def __init__(
            self,
            method: Text = MappingMethod.RULE_BASED,
            case_sensitive: bool = True,
            export: bool = False,
            quiet_mode: bool = False,
    ) -> None:
        self.method = method
        self.case_sensitive = case_sensitive
        self.export = export
        self.quiet_mode = quiet_mode
        logger.debug('Initialized the SEETM mapper')

    def map_and_persist(self):
        raise NotImplementedError()

    def map(
            self,
            data_instance: Text = None,
            token_list: bool = False,
    ) -> Union[Text, Tuple[Text, List]]:
        try:
            if self.method not in [
                MappingMethod.IPA,
                MappingMethod.RULE_BASED
            ]:
                raise NotImplementedError()

            if not data_instance:
                raise InvalidDataInstanceException()

            if self.method == MappingMethod.IPA:
                en_to_phonetics_mapper = EnglishToPhoneticsMapper()

                # tokenize
                tokens = tokenize(data_instance)

                # replacing from user-provided pronunciations
                tokens = [
                    en_to_phonetics_mapper.map(token=token)
                    if len(EN_PATTERN.findall(token)) == 1 else token
                    for token in tokens
                ]

                # converting the rest of remaining english
                # words to IPA representation
                mapped_tokens = [
                    {
                        "token": t,
                        "status": ipa.isin_cmu(t),
                        "ipa": ipa.convert(t) if ipa.isin_cmu(t) else t
                    }
                    for t
                    in tokens
                    if t
                ]

                # converting the IPA representation to
                # the appropriate sinhala representation
                mapped_token_list = list()
                for token in mapped_tokens:
                    if token["status"]:
                        mapped_token = IPAToSinhalaMapper.replace(
                            text=token["token"],
                            ipa_text=token["ipa"],
                            map_phrases=True
                        )
                    else:
                        mapped_token = token["token"]
                    token["mapped_token"] = mapped_token

                    if token_list:
                        mapped_token_list.append({
                            "token": token["token"],
                            "mapped_token": mapped_token,
                        })

                # return the combined tokens
                mapped_text = " ".join(
                    [token["mapped_token"]
                     for token
                     in mapped_tokens]
                ) if mapped_tokens else ""

                return mapped_text, mapped_token_list

            elif self.method == MappingMethod.RULE_BASED:
                token_to_token_mapper = TokenToTokenMapper(case_sensitive = self.case_sensitive)
                mapped_text = token_to_token_mapper.map(text=data_instance)

                return mapped_text
            else:
                raise InvalidMappingMethodException()
        except Exception as e:
            raise MapperException(e)

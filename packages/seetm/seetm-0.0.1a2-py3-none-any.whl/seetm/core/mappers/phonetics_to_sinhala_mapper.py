import logging

import regex

from seetm.core.maps.phonetics_to_sinhala_maps import (
    SI_VOWEL_KEYS,
    SI_VOWEL_PURE_MAP,
    SI_VOWEL_SUFFIX_MAP,
    SI_CONSONANT_KEYS,
    SI_CONSONANT_MAP,
    SI_NON_JOINING_KEYS,
    SI_NON_JOINING_MAP,
    SI_SPECIAL_KEYS,
    SI_SPECIAL_MAP,
)

logger = logging.getLogger(__name__)


class PhoneticsToSinhalaMapper:
    @staticmethod
    def convert(text):
        # Replacing non-joining characters
        for nj_char in SI_NON_JOINING_KEYS:
            en_pattern = nj_char
            si_pattern = SI_NON_JOINING_MAP[nj_char]
            text = regex.sub(en_pattern, si_pattern, text)

        # Replacing special consonants
        for sp_char in SI_SPECIAL_KEYS:
            for con_char in SI_CONSONANT_KEYS:
                en_pattern = con_char + sp_char
                si_pattern = SI_CONSONANT_MAP[con_char] + SI_SPECIAL_MAP[sp_char]
                text = regex.sub(en_pattern, si_pattern, text)

        # Replacing consonants + Rakaransha + vowel modifiers
        for con_char in SI_CONSONANT_KEYS:
            for v_char in SI_VOWEL_KEYS:
                en_pattern = con_char + "r" + v_char
                si_pattern = SI_CONSONANT_MAP[con_char] + "්‍ර" + SI_VOWEL_SUFFIX_MAP[v_char]
                text = regex.sub(en_pattern, si_pattern, text)

            en_pattern = con_char + "r"
            si_pattern = SI_CONSONANT_MAP[con_char] + "්‍ර"
            text = regex.sub(en_pattern, si_pattern, text)

        # Replacing consonants + vowel modifiers
        for con_char in SI_CONSONANT_KEYS:
            for v_char in SI_VOWEL_KEYS:
                en_pattern = con_char + v_char
                si_pattern = SI_CONSONANT_MAP[con_char] + SI_VOWEL_SUFFIX_MAP[v_char]
                text = regex.sub(en_pattern, si_pattern, text)

        # Replacing consonants + HAL
        for con_char in SI_CONSONANT_KEYS:
            en_pattern = con_char
            si_pattern = SI_CONSONANT_MAP[con_char] + "්"
            text = regex.sub(en_pattern, si_pattern, text)

        # Replacing vowels
        for v_char in SI_VOWEL_KEYS:
            en_pattern = v_char
            si_pattern = SI_VOWEL_PURE_MAP[v_char]
            text = regex.sub(en_pattern, si_pattern, text)

        return text


if __name__ == "__main__":
    logger.debug("Started testing the phonetic mapper...")
    print(PhoneticsToSinhalaMapper.convert(
        """
        dhis iis a test
        """
    ))

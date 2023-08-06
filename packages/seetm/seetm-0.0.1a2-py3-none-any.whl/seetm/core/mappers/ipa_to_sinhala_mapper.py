import logging
from copy import deepcopy
from typing import Text

import regex

from seetm.core.maps.ipa_to_sinhala_maps import (
    IPA_SI_VOWEL_KEYS,
    IPA_SI_VOWEL_SUFFIX_MAP,
    IPA_SI_CONSONANT_KEYS,
    IPA_SI_CONSONANT_MAP,
    EXACT_MATCH_KEYS,
    EXACT_MATCH_MAP,
)

logger = logging.getLogger(__name__)


class IPAToSinhalaMapper:
    @staticmethod
    def replace(text: Text, ipa_text: Text, map_phrases: bool = True) -> Text:
        word = str.lower(deepcopy(text))
        chars = str.lower(deepcopy(ipa_text))
        # STAGE 0
        # maps exact matches if set to true
        if map_phrases:
            # exact matches
            if word in EXACT_MATCH_KEYS:
                return EXACT_MATCH_MAP[word]

            # prefixes
            chars = regex.sub(r"^əˈwɔrd", "අවෝර්ඩ්", chars)
            chars = regex.sub(r"^ˌjunəˈvər", "යුනිවර්", chars)
            chars = regex.sub(r"^ækt", "ඇක්ට්", chars)
            chars = regex.sub(r"^ˈkɑmən", "කොමන්", chars)
            chars = regex.sub(r"^əˌsoʊʃi", "ඇසෝසි", chars)
            chars = regex.sub(r"^əˈkrɛdɪt", "ඇක්‍රෙඩිට්", chars)
            chars = regex.sub(r"^prəˈfɛʃən", "ප්‍රොෆෙශන්", chars)
            # terms
            chars = regex.sub(r"ˈnæʃənɑl", "නැශනල්", chars)
            chars = regex.sub(r"ˈnæʃənəl", "නැශනල්", chars)
            chars = regex.sub(r"^ˈpərsɪnəl$", "පර්සනල්", chars)
            chars = regex.sub(r"ʤɑb", "ජොබ්", chars)
            # suffixes
            chars = regex.sub(r"tut$", "ටියුට්", chars)
            chars = regex.sub(r"ˈtuʃən$", "ටියුෂන්", chars)
            chars = regex.sub(r"tud$", "ටියුඩ්", chars)
            chars = regex.sub(r"ɑləʤi$", "ඔලොජි", chars)
            chars = regex.sub(r"səti$", "සිටි", chars)
            chars = regex.sub(r"ˈeɪʃən$", "යේශන්", chars)
            chars = regex.sub(r"sətiz$", "සිටීස්", chars)
            chars = regex.sub(r"com$", "කොම්", chars)

        # STAGE 1
        # diphthongs
        chars = regex.sub(r"eɪ", "ඒ", chars)  # එයි
        chars = regex.sub(r"aɪ", "අයි", chars)
        chars = regex.sub(r"aʊ", "අව්", chars)
        chars = regex.sub(r"ɔɪ", "ඕ", chars)
        chars = regex.sub(r"oʊ", "ඕ", chars)  # ඔයි
        # monophthongs + stress
        chars = regex.sub(r"ˈæ", "ඇ", chars)
        chars = regex.sub(r"ˌæ", "ඇ", chars)
        # monophthongs
        chars = regex.sub(r"i", "ඊ", chars)
        chars = regex.sub(r"u", "ඌ", chars)
        chars = regex.sub(r"ɪ", "ඉ", chars)
        chars = regex.sub(r"ʊ", "උ", chars)
        chars = regex.sub(r"ə", "අ", chars)
        chars = regex.sub(r"ɛ", "එ", chars)
        chars = regex.sub(r"ɝ", "අර්", chars)
        chars = regex.sub(r"æ", "ඈ", chars)
        chars = regex.sub(r"ɑ", "ආ", chars)
        # consonants
        chars = regex.sub(r"tʃ", "ච්", chars)
        chars = regex.sub(r"dʒ", "ජ්", chars)
        chars = regex.sub(r"p", "ප්", chars)
        chars = regex.sub(r"b", "බ්", chars)
        chars = regex.sub(r"t", "ට්", chars)
        chars = regex.sub(r"d", "ඩ්", chars)
        chars = regex.sub(r"k", "ක්", chars)
        chars = regex.sub(r"g", "ග්", chars)
        chars = regex.sub(r"θ", "ත්", chars)
        chars = regex.sub(r"ð", "ද්", chars)
        chars = regex.sub(r"f", "ෆ්", chars)
        chars = regex.sub(r"v", "ව්", chars)
        chars = regex.sub(r"s", "ස්", chars)
        chars = regex.sub(r"z", "ස්", chars)
        chars = regex.sub(r"ʃ", "ශ්", chars)
        chars = regex.sub(r"ʒ", "ෂ්", chars)
        chars = regex.sub(r"w", "ව්", chars)
        chars = regex.sub(r"ɫ", "ල්", chars)
        chars = regex.sub(r"m", "ම්", chars)
        chars = regex.sub(r"n", "න්", chars)
        chars = regex.sub(r"ŋ", "න්ග්", chars)
        chars = regex.sub(r"ɹ", "ර්", chars)
        chars = regex.sub(r"j", "ය්", chars)
        chars = regex.sub(r"h", "හ්", chars)
        # modern
        chars = regex.sub(r"l", "ල්", chars)
        chars = regex.sub(r"r", "ර්", chars)
        chars = regex.sub(r"ʤ", "ජ්", chars)
        chars = regex.sub(r"ɔ", "අව්", chars)

        # STAGE 2
        # stress (primary(') or secondary(,))
        # remove remaining stress marks
        chars = regex.sub(r"ˈ", "", chars)
        chars = regex.sub(r"ˌ", "", chars)

        # STAGE 3
        # combine consonants and vowels that
        # appear next to each other
        for consonant in IPA_SI_CONSONANT_KEYS:
            for vowel in IPA_SI_VOWEL_KEYS:
                # consonant + ර් + vowel
                pattern_before = consonant + 'ර්' + vowel
                pattern_after = IPA_SI_CONSONANT_MAP[consonant] + "්‍ර" + IPA_SI_VOWEL_SUFFIX_MAP[vowel]
                chars = regex.sub(pattern_before, pattern_after, chars)

                # consonant + vowel
                pattern_before = consonant + vowel
                pattern_after = IPA_SI_CONSONANT_MAP[consonant] + IPA_SI_VOWEL_SUFFIX_MAP[vowel]
                chars = regex.sub(pattern_before, pattern_after, chars)
        return chars

import logging
from difflib import SequenceMatcher
from typing import List, Text

from seetm.shared.exceptions.core import (
    InvalidNumberOfTokensException,
)

logger = logging.getLogger(__name__)


def similarity(tokens: List[Text], inspect: bool = False) -> float:
    if len(tokens) != 2:
        raise InvalidNumberOfTokensException()

    token_1 = tokens[0]
    token_2 = tokens[1]

    sequence_matcher = SequenceMatcher(a=token_1, b=token_2)
    similarity_score = sequence_matcher.ratio()

    # displaying the similarity score if required
    if inspect:
        print(similarity_score)
    return similarity_score


if __name__ == "__main__":
    logger.debug("Testing the Sequence similarity score...")
    score = similarity(["dog", "dog"], inspect=True)

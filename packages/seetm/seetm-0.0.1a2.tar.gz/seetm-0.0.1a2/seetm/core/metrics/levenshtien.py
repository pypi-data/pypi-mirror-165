import logging
from typing import List, Text

import numpy

from seetm.shared.exceptions.core import (
    InvalidNumberOfTokensException,
)

logger = logging.getLogger(__name__)


def distance(tokens: List[Text], inspect: bool = False) -> int:
    if len(tokens) != 2:
        raise InvalidNumberOfTokensException()

    token_1 = tokens[0]
    token_2 = tokens[1]
    side_1 = len(token_1) + 1
    side_2 = len(token_2) + 1

    # initializing the distance matrix
    distance_matrix = numpy.zeros((side_1, side_2), int)
    for y in range(side_1):
        distance_matrix[y][0] = y
    for x in range(side_2):
        distance_matrix[0][x] = x

    # filling the distance matrix row by row
    for y in range(1, side_1):
        for x in range(1, side_2):
            insert_op = distance_matrix[y-1][x]
            delete_op = distance_matrix[y][x-1]
            replace_op = distance_matrix[y-1][x-1]

            if token_1[y-1] == token_2[x-1]:
                distance_matrix[y][x] = replace_op
            else:
                distance_matrix[y][x] = \
                    min([insert_op, delete_op, replace_op]) + 1

    # displaying the distance matrix if required
    if inspect:
        print(distance_matrix)
    return int(distance_matrix[side_1-1][side_2-1])


if __name__ == "__main__":
    logger.debug("Testing the Levenshtein distance...")
    print(distance(["dog", "ok"], inspect=True))

import json
import logging
import os
from typing import NoReturn, Dict

from seetm.shared.constants import (
    Encoding,
    FilePermission,
    DEFAULT_EVALUATION_RESULTS_PATH,
)
from seetm.shared.exceptions.core import (
    EvaluationPersistException,
)
from seetm.utils.io import get_timestamp_str

logger = logging.getLogger(__name__)


class Evaluation:
    def __init__(self, evaluation: Dict) -> None:
        self.name = f"seetm_eval_{get_timestamp_str()}.json"
        self.content = evaluation

    def persist(self, indent: int = 4) -> NoReturn:
        try:
            with open(
                    os.path.join(DEFAULT_EVALUATION_RESULTS_PATH, self.name),
                    encoding=Encoding.UTF8,
                    mode=FilePermission.WRITE
            ) as evaluation_file:
                json.dump(
                    self.content,
                    evaluation_file,
                    ensure_ascii=False,
                    indent=indent
                )
                logger.debug(f"Evaluation {self.name} "
                             f"was persisted")
        except Exception:
            logger.error(f"Failed to persist the specified "
                         f"SEETM evaluation {self.name}")
            raise EvaluationPersistException()

    def inspect(self):
        print(json.dumps(self.content, ensure_ascii=False, indent=4))

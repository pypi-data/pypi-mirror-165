import json
import logging
import os
from typing import Union, Text, NoReturn, List, Dict

from seetm.shared.constants import (
    DEFAULT_EXPORTABLE_PATH,
    Encoding,
    FilePermission,
)
from seetm.shared.exceptions.core import (
    ExportableInitializationException, ExportablePersistException,
)
from seetm.utils.io import get_timestamp_str

logger = logging.getLogger(__name__)


class Exportable:
    def __init__(self, exportable: Union[List, Text]) -> None:
        if isinstance(exportable, str):
            self.name = exportable
            self.content = self._initialize(exportable=exportable)
        else:
            self.name = f"seetm_export_{get_timestamp_str()}.json"
            self.content = exportable

    @staticmethod
    def _initialize(exportable: Text) -> Dict:
        try:
            if len(os.path.split(exportable)) != 1:
                raise ExportableInitializationException()

            with open(
                    os.path.join(DEFAULT_EXPORTABLE_PATH, exportable),
                    encoding=Encoding.UTF8,
                    mode=FilePermission.READ
            ) as exportable_file:
                exportable_content = json.load(exportable_file)

            return exportable_content
        except Exception:
            logger.error(f"Failed to initialize the specified "
                         f"SEETM exportable {exportable}")
            raise ExportableInitializationException()

    def persist(self, indent: int = 4) -> NoReturn:
        try:
            with open(
                    os.path.join(DEFAULT_EXPORTABLE_PATH, self.name),
                    encoding=Encoding.UTF8,
                    mode=FilePermission.WRITE
            ) as exportable_file:
                json.dump(
                    self.content,
                    exportable_file,
                    ensure_ascii=False,
                    indent=indent
                )
                logger.debug(f"Exportable {self.name} "
                             f"was persisted")
        except Exception:
            logger.error(f"Failed to persist the specified "
                         f"SEETM exportable {self.name}")
            raise ExportablePersistException()

    def inspect(self):
        print(json.dumps(self.content, ensure_ascii=False, indent=4))

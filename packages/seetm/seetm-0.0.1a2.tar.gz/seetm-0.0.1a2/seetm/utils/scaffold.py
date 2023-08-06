import logging
import os
import shutil
from typing import Text, NoReturn

import pkg_resources

from seetm.shared.constants import (
    DEFAULT_INIT_SRC_DIR_NAME,
    DEFAULT_INIT_DEST_DIR_NAME,
    DEFAULT_INIT_CACHE_DIR_NAME,
    DEFAULT_INIT_FILES_TO_EXCLUDE,
    ALLOWED_INIT_DIR_NAMES,
    DestinationDirType,
    RASA_DIRS_IN_SEETM_INIT,
)
from seetm.shared.exceptions.io import (
    InvalidInitDirException,
    ProjectExistsException,
)
from seetm.utils.io import (
    get_timestamp_str,
    get_seetm_init_caches,
    get_existing_toplevel_file_list,
)

logger = logging.getLogger(__name__)


class SEETMInit:
    def __init__(self, src: Text = DEFAULT_INIT_SRC_DIR_NAME):
        self._src = src
        self.src_path = None
        self.cache_path_timestamped = None
        self.cache_path_timestamped_path = None

    def build_scaffold(
            self,
            dest_path: Text = DEFAULT_INIT_DEST_DIR_NAME
    ) -> NoReturn:

        dest_path = str(dest_path).strip()
        if not dest_path or str(dest_path).strip() in ALLOWED_INIT_DIR_NAMES:
            dest_path = DEFAULT_INIT_DEST_DIR_NAME

        try:
            self.src_path = pkg_resources.resource_filename(__name__, self._src)
            self.cache_path_timestamped = DEFAULT_INIT_CACHE_DIR_NAME + get_timestamp_str()
            self.cache_path_timestamped_path = os.path.join(dest_path, self.cache_path_timestamped) + "\\"

            # removing existing caches
            cached_init_list = get_seetm_init_caches(dest_path)
            for elem in cached_init_list:
                shutil.rmtree(elem)

            dest_dir_type = self._verify_destination_dir(dest_path)
            if dest_dir_type == DestinationDirType.RASA:
                logger.info("The initialization directory is already a rasa directory. "
                            "only SEETM files will be created.")
                shutil.copytree(
                    src=self.src_path,
                    dst=self.cache_path_timestamped_path,
                    ignore=shutil.ignore_patterns('__pycache__', '__main__.py', 'data'),
                )
            elif dest_dir_type == DestinationDirType.VALID or dest_dir_type == DestinationDirType.EMPTY:
                shutil.copytree(
                    src=self.src_path,
                    dst=self.cache_path_timestamped_path,
                    ignore=shutil.ignore_patterns('__pycache__', '__main__.py'),
                )
            elif dest_dir_type == DestinationDirType.SEETM:
                raise ProjectExistsException("The initialization directory already contains a SEETM project. "
                                             "Initialization aborted.")
            else:
                raise InvalidInitDirException("The initialization directory seems invalid. "
                                              "Initialization aborted.")

            dir_contents = get_existing_toplevel_file_list(self.cache_path_timestamped_path)
            for elem in dir_contents:
                if elem in DEFAULT_INIT_FILES_TO_EXCLUDE:
                    continue

                abs_src_path = os.path.join(self.cache_path_timestamped_path, elem)
                rel_dst_path = os.path.join(dest_path, elem)
                shutil.move(src=abs_src_path, dst=rel_dst_path)
            shutil.rmtree(path=self.cache_path_timestamped_path)
            os.remove(path=os.path.join("./", "__init__.py"))

            logger.info("Initialized a new SEETM project.")
        except Exception as e:
            logger.error(f"Initializing SEETM project failed. more info: {e}")
            exit()

    def _verify_destination_dir(self, dest_path: Text = None) -> Text:
        if not dest_path:
            return DestinationDirType.INVALID

        existing_src_files = get_existing_toplevel_file_list(
            self.src_path,
            exclude=DEFAULT_INIT_FILES_TO_EXCLUDE
        )
        existing_dest_files = get_existing_toplevel_file_list(
            dir_path=dest_path,
            exclude=DEFAULT_INIT_FILES_TO_EXCLUDE
        )

        if not existing_dest_files:
            return DestinationDirType.EMPTY
        elif existing_dest_files:
            rasa_overlap = list(set(RASA_DIRS_IN_SEETM_INIT).intersection(set(existing_dest_files)))
            seetm_overlap = list(set(list(set(existing_src_files).intersection(set(existing_dest_files))))
                                 .difference(set(RASA_DIRS_IN_SEETM_INIT)))

            if seetm_overlap:
                logger.warning(f"Found overlapping SEETM files and/or directories: {', '.join(seetm_overlap)}")
                return DestinationDirType.SEETM
            elif rasa_overlap:
                logger.warning(f"Found overlapping RASA files and/or directories: {', '.join(rasa_overlap)}")
                return DestinationDirType.RASA
        return DestinationDirType.VALID

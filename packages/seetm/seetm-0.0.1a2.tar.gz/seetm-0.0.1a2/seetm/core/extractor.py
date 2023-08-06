import json
import logging
import os.path
from typing import NoReturn, Dict, List, Tuple

import eng_to_ipa as ipa
import regex
from rich.progress import track
from ruamel.yaml.comments import (
    CommentedMap as OrderedDict,
    CommentedSeq as OrderedList,
)

from seetm.shared.constants import (
    Config,
    Encoding,
    FilePermission,
    DEFAULT_NLU_EXAMPLES_TAG,
    ENGLISH_TOKEN_PATTERN,
    DEFAULT_EVALUATION_DATA_PATH,
    EN_TO_PHONETICS_MAP_PATH,
    TOKEN_TO_TOKEN_MAP_PATH, YAML_EXTENSIONS,
)
from seetm.shared.exceptions.core import (
    EvaluationDatasetExportException,
    MappingExportException, ExtractorCleanupException,
)
from seetm.shared.exceptions.io import (
    EmptyNLUDatasetException,
    InvalidNLUDatasetException,
)
from seetm.utils.io import (
    dir_exists,
    get_rasa_testing_data,
    write_yaml_file,
    file_exists,
    delete_top_level_files,
    delete_file,
    read_yaml_file,
)
from seetm.utils.text_preprocessing import tokenize

logger = logging.getLogger(__name__)
EN_PATTERN = regex.compile(ENGLISH_TOKEN_PATTERN)


class SEETMExtractor:
    def __init__(
            self,
            configs: Dict,
            persist: bool = False,
            clean: bool = False,
            quiet_mode: bool = False,
    ) -> NoReturn:
        self.data_path = configs[Config.BASE_CONFIGS_KEY][Config.DATA_PATH_KEY]
        self.persist = persist
        self.clean = clean
        self.quiet_mode = quiet_mode
        self.progress_description_width = 30

    def extract(self) -> Tuple[List, List]:
        logger.debug("Initializing SEETM Extractor...")

        # loading the NLU dataset
        if not dir_exists(self.data_path):
            raise InvalidNLUDatasetException()

        nlu_dataset = get_rasa_testing_data(
            testing_data_dir=self.data_path,
            preserve_location=True,
        )

        if not nlu_dataset:
            EmptyNLUDatasetException()

        nlu_intents = nlu_dataset.keys() if self.quiet_mode else \
            track(
                nlu_dataset.keys(),
                description=f"{'Loading NLU dataset:':{self.progress_description_width}}"
            )

        nlu_example_list = list()
        for intent in nlu_intents:
            for example in nlu_dataset[intent][DEFAULT_NLU_EXAMPLES_TAG]:
                nlu_example_list.append(example)

        # cleaning existing files if requested
        if self.clean:
            try:
                delete_file(file_path=[EN_TO_PHONETICS_MAP_PATH, TOKEN_TO_TOKEN_MAP_PATH])
                delete_top_level_files(dir_path=DEFAULT_EVALUATION_DATA_PATH, ext=YAML_EXTENSIONS)
            except Exception as e:
                raise ExtractorCleanupException(e)

        mappable_token_list = list()
        unmappable_token_list = list()
        if not self.quiet_mode:
            nlu_example_list = track(
                nlu_example_list,
                description=f"{'Extracting tokens:':{self.progress_description_width}}"
            )
        for example in nlu_example_list:
            tokens = tokenize(instance=example)
            tokens = [str.lower(t) for t in tokens]
            for token in tokens:
                if len(EN_PATTERN.findall(token)) == 1:
                    if ipa.isin_cmu(token):
                        mappable_token_list.append(token) if token not in mappable_token_list else None
                    else:
                        unmappable_token_list.append(token) if token not in unmappable_token_list else None

        if self.persist:
            self._persist_evaluation_dataset(token_list=mappable_token_list)
            self._persist_en_to_phonetics_map(token_list=unmappable_token_list)
            self._persist_token_to_token_map(token_list=mappable_token_list + unmappable_token_list)
        else:
            if not self.quiet_mode:
                logger.warning("Evaluation dataset and maps will not be "
                               "persisted as `persist` was set to false`")

        return mappable_token_list, unmappable_token_list

    def _persist_evaluation_dataset(self, token_list: List) -> NoReturn:
        try:
            if not token_list:
                logger.warning("Not enough tokens were discovered "
                               "to generate the evaluation dataset")
                return

            # generate map skeletons
            number_of_tokens = len(token_list)
            try:
                existing_dataset_yml = read_yaml_file(
                    yaml_file=os.path.join(DEFAULT_EVALUATION_DATA_PATH, "token_eval.yml"),
                    encoding=Encoding.UTF8,
                    mode=FilePermission.READ,
                    version_check=False,
                )
            except OSError:
                existing_dataset_yml = {}
            existing_dataset = json.loads(json.dumps(existing_dataset_yml, ensure_ascii=False))
            existing_tokens = {
                mapping["token"]: mapping["test_token"] for mapping in existing_dataset["eval"]
                if mapping["token"] not in existing_dataset
            } if existing_dataset else dict()

            token_eval_dataset = OrderedDict({"eval": OrderedList()})
            if not self.quiet_mode:
                token_list = track(
                    token_list,
                    description=f"{'Generating Evaluation Dataset:':{self.progress_description_width}}"
                )
            for token in token_list:
                test_token = existing_tokens[token] if token in existing_tokens.keys() else ""
                token_eval_dataset.get("eval").append(
                    OrderedDict({
                        "token": token,
                        "test_token": test_token,
                    })
                )

            # inserting line breaks
            for key in range(1, len(token_eval_dataset.get("eval"))):
                token_eval_dataset["eval"].yaml_set_comment_before_after_key(
                    key=key,
                    before='\n'
                )

            write_yaml_file(
                file_path=os.path.join(DEFAULT_EVALUATION_DATA_PATH, "token_eval.yml"),
                content=token_eval_dataset,
                encoding=Encoding.UTF8,
                mode=FilePermission.WRITE,
                preserve_quotes=True,
            )
            if not self.quiet_mode:
                logger.info("Evaluation dataset skeleton was updated. Make sure to "
                            "manually add test_token mappings before evaluating")
                logger.info(f"Number of evaluation tokens persisted: {number_of_tokens}")
        except Exception as e:
            raise EvaluationDatasetExportException(e)

    def _persist_en_to_phonetics_map(self, token_list: List) -> NoReturn:
        try:
            if not token_list:
                logger.warning("Not enough tokens were discovered "
                               "to update IPA mappings")
                return

            # load existing map
            if file_exists(EN_TO_PHONETICS_MAP_PATH):
                with open(EN_TO_PHONETICS_MAP_PATH, encoding=Encoding.UTF8, mode=FilePermission.READ) as map_content:
                    existing_map = json.load(map_content)
            else:
                existing_map = {}
            existing_map = existing_map or {}
            updated_tokens = list()

            if not self.quiet_mode:
                token_list = track(
                    token_list,
                    description=f"{'Updating Map [Phonetics]:':{self.progress_description_width}}"
                )
            for token in token_list:
                if token not in existing_map.keys():
                    existing_map.update({token: ""})
                    updated_tokens.append(token)

            with open(EN_TO_PHONETICS_MAP_PATH, encoding=Encoding.UTF8, mode=FilePermission.WRITE) as updated_map:
                json.dump(existing_map, updated_map, ensure_ascii=False, indent=4)

            if not self.quiet_mode:
                logger.info("en_to_phonetics map was updated. Make sure to "
                            "manually add missing mappings before IPA mapping tasks")
                logger.info(f"Number of tokens updated: {len(updated_tokens)}")
        except Exception as e:
            raise MappingExportException(e)

    def _persist_token_to_token_map(self, token_list: List) -> NoReturn:
        try:
            if not token_list:
                logger.warning("Not enough tokens were discovered "
                               "to update Rule-based mappings")
                return

            # load existing map
            if file_exists(TOKEN_TO_TOKEN_MAP_PATH):
                with open(TOKEN_TO_TOKEN_MAP_PATH, encoding=Encoding.UTF8, mode=FilePermission.READ) as map_content:
                    existing_map = json.load(map_content)
            else:
                existing_map = {}
            existing_map = existing_map or {}
            updated_tokens = list()

            if not self.quiet_mode:
                token_list = track(
                    token_list,
                    description=f"{'Updating Map [Rule-based]:':{self.progress_description_width}}"
                )
            existing_keys = existing_map.keys() or list()
            existing_values = list()

            for key, values in existing_map.items():
                existing_values += values

            for token in token_list:
                if token in existing_keys or token in existing_values:
                    continue
                else:
                    existing_map.update({token: [token]})
                    updated_tokens.append(token)

            with open(TOKEN_TO_TOKEN_MAP_PATH, encoding=Encoding.UTF8, mode=FilePermission.WRITE) as updated_map:
                json.dump(existing_map, updated_map, ensure_ascii=False, indent=4)

            if not self.quiet_mode:
                logger.info("token_to_token map was updated. Make sure to manually "
                            "add missing mappings before Rule-based mapping tasks")
                logger.info(f"Number of tokens updated: {len(updated_tokens)}")
        except Exception as e:
            raise MappingExportException(e)

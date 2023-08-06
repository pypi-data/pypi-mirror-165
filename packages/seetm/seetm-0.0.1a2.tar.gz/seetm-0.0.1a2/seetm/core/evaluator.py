import logging
from typing import NoReturn, Dict, Text, Union, List, Iterable

from rich.progress import track

import seetm.core.extractor
from seetm.core.extractor import SEETMExtractor
from seetm.core.word2vec import (
    Word2VecModel,
)
from seetm.core.metrics.levenshtien import distance
from seetm.core.metrics.sequence_matcher import similarity
from seetm.core.token_mapper import TokenMapper
from seetm.shared.constants import (
    MappingMethod,
    Config,
    DEFAULT_NLU_LOCATION_TAG,
    DEFAULT_EVAL_TOKEN_TAG,
    DEFAULT_EVAL_TEST_TOKEN_TAG,
    DEFAULT_NLU_INTENT_TAG,
    Metrics, EvaluationLevel,
    DEFAULT_NLU_EXAMPLES_TAG,
    DEFAULT_DATA_PATH, DEFAULT_EVALUATION_DATA_PATH,
)
from seetm.shared.evaluation import Evaluation
from seetm.shared.exceptions.base import SEETMException
from seetm.shared.exceptions.core import (
    SEETMCoreException,
    MapperException,
    InvalidDataInstanceException,
    ExportableInitializationException,
    InvalidEvaluationLevelException,
    InvalidEvaluationMethodException,
    ZeroMappedTokensException,
    ZeroValidTokensException,
    OutDatedEvaluationDatasetException,
)
from seetm.shared.exceptions.io import (
    SEETMIOException,
    EmptyNLUDatasetException,
    InvalidFileExtensionException,
    InvalidNLUDatasetException,
    YAMLFormatException,
    EvalFileNotFoundException,
    InvalidEvalDatasetException,
    EmptyEvalDatasetException,
)
from seetm.utils.io import (
    dir_exists,
    get_rasa_testing_data,
    get_seetm_eval_data,
)

logger = logging.getLogger(__name__)


class SEETMEvaluator:
    def __init__(
            self,
            configs: Dict,
            level: Text,
            epochs: int,
            persist: bool = False,
            quiet_mode: bool = False,
    ) -> NoReturn:
        self.data_path = configs[Config.BASE_CONFIGS_KEY][Config.DATA_PATH_KEY]
        self.method = configs[Config.BASE_CONFIGS_KEY][Config.METHOD_KEY]
        self.metric = configs[Config.BASE_CONFIGS_KEY][Config.METRIC_KEY]
        self.level = level
        self.epochs = epochs
        self.persist = persist
        self.quiet_mode = quiet_mode
        self.token_mapper = TokenMapper(
            method=self.method,
            quiet_mode=self.quiet_mode
        )
        self.extractor = SEETMExtractor(
            configs=configs,
            persist=False,
            clean=False,
            quiet_mode=False
        )
        self.progress_description_width = 30

    def _map(self, instance: Text) -> Text:
        return self.token_mapper.map(
            data_instance=instance,
            token_list=True
        )

    def _wrap_progress(
            self,
            iterable: Union[List, Dict, Iterable],
            description: Text,
            total: Union[int, float]
    ) -> Union[List, Dict, Iterable]:
        if self.quiet_mode:
            return iterable
        else:
            return track(sequence=iterable, description=description, total=total)

    def _get_eval_tokens(self):
        eval_dataset = get_seetm_eval_data(
            eval_data_dir=DEFAULT_EVALUATION_DATA_PATH,
            preserve_location=True,
        )

        if not eval_dataset:
            raise EmptyEvalDatasetException()

        nlu_tokens = self.extractor.extract()

        eval_tokens_dict = {
            element["token"]: element["test_token"]
            for element in eval_dataset
            if str.strip(element["token"]) and str.strip(element["test_token"])
        }
        eval_tokens = [
            element["token"]
            for element in eval_dataset
            if str.strip(element["token"]) and str.strip(element["test_token"])
        ]
        invalid_eval_tokens = [
            element["token"]
            for element in eval_dataset
            if not str.strip(element["token"]) or not str.strip(element["test_token"])
        ]
        outdated_eval_tokens = set(eval_tokens).difference(set(nlu_tokens[0]))

        logger.info(f"Found {len(eval_tokens)} valid evaluation tokens out of {len(eval_dataset)}")

        if len(eval_tokens) == 0:
            raise ZeroValidTokensException()

        if invalid_eval_tokens:
            logger.warning(f"Invalid tokens: {', '.join(invalid_eval_tokens)}")

        if outdated_eval_tokens:
            logger.warning(f"Out-dated tokens: {', '.join(outdated_eval_tokens)}")
            raise OutDatedEvaluationDatasetException()

        if invalid_eval_tokens:
            logger.warning("Use `seetm extract` to generate an up-to-date evaluation dataset "
                           "skeleton before running `seetm evaluate`")
        return eval_tokens_dict

    def evaluate(self) -> NoReturn:
        logger.debug("Initializing SEETM Evaluator...")

        # Deprecations, Errors and Warnings
        # for SEETM Evaluator arguments
        if self.level == EvaluationLevel.TOKEN and self.method == MappingMethod.RULE_BASED:
            logger.error("Token level evaluation cannot be performed when "
                         "'rule-based' is selected as the mapping method.")
            exit()

        if not dir_exists(self.data_path):
            raise InvalidEvalDatasetException()

        # retrieving the eval tokens
        eval_tokens_dict = self._get_eval_tokens()
        eval_tokens_dict_keys = self._wrap_progress(
            iterable=eval_tokens_dict.keys(),
            description=f"{'Evaluating tokens:':{self.progress_description_width}}",
            total=len(eval_tokens_dict)
        )

        if self.level == EvaluationLevel.TOKEN:
            mapped_list = list()
            score_list = list()
            exact_matches = 0
            for token in eval_tokens_dict_keys:
                test_token = eval_tokens_dict[token]
                mapped_token = self._map(instance=token)

                if isinstance(mapped_token, tuple):
                    mapped_token = mapped_token[0]

                if self.metric == Metrics.EDIT_DISTANCE:
                    score = distance(
                        tokens=[test_token, mapped_token],
                        inspect=False
                    )
                    if score == 0:
                        exact_matches += 1

                elif self.metric == Metrics.SEQUENCE_MATCHING:
                    score = similarity(
                        tokens=[test_token, mapped_token],
                        inspect=False
                    )
                    if score == 1.0:
                        exact_matches += 1
                else:
                    score = None

                score_list.append(score)

                mapped_list.append({
                    "token": token,
                    "test_token": test_token,
                    "mapped_token": mapped_token,
                    "score": score,
                })

            # embedding summarized evaluation statistics
            average_score = sum(score_list) / len(score_list) if len(score_list) > 0 else None
            evaluation_obj = {
                "evaluation_level": self.level,
                "method": self.method,
                "metric": self.metric,
                "exact_matches": exact_matches,
                "total_matches": len(mapped_list),
                "exact_match_rate": exact_matches / len(mapped_list) if len(mapped_list) > 0 else None,
            }
            if self.metric == Metrics.EDIT_DISTANCE:
                evaluation_obj.update({
                    "average_edit_distance": average_score,
                    "maximum_edit_distance": max(score_list),
                    "evaluated_pairs": mapped_list,
                })
            else:
                evaluation_obj.update({
                    "average_similarity_score": average_score,
                    "minimum_similarity_score": min(score_list),
                    "evaluated_pairs": mapped_list,
                })

            evaluation = Evaluation(evaluation=evaluation_obj)
            if self.persist:
                evaluation.persist()
                logger.info(f"Evaluation results were persisted as '{evaluation.name}'")

        elif self.level == EvaluationLevel.VECTOR:
            # loading NLU dataset
            if not dir_exists(self.data_path):
                raise InvalidNLUDatasetException()

            nlu_dataset = get_rasa_testing_data(
                testing_data_dir=self.data_path,
                preserve_location=True,
            )

            if not nlu_dataset:
                EmptyNLUDatasetException()

            nlu_dataset_keys = self._wrap_progress(
                iterable=nlu_dataset.keys(),
                description=f"{'Extracting NLU examples:':{self.progress_description_width}}",
                total=len(nlu_dataset)
            )

            nlu_example_list = list()
            for intent in nlu_dataset_keys:
                for example in nlu_dataset[intent][DEFAULT_NLU_EXAMPLES_TAG]:
                    nlu_example_list.append(example)

            # train a word-to-vec model for NLU data
            nlu_model = Word2VecModel(model_name="nlu_model", dataset=nlu_example_list, epochs=self.epochs)
            nlu_model.train()

            # train word-to-vec models on IPA/Rule-based mapped data
            if self.method == MappingMethod.IPA:
                nlu_ipa_mapped_example_list = list()
                mapped_token_list = list()
                nlu_example_list = self._wrap_progress(
                    iterable=nlu_example_list,
                    description=f"{'Mapping NLU to IPA:':{self.progress_description_width}}",
                    total=len(nlu_example_list)
                )

                for example in nlu_example_list:
                    mapped_example = self._map(instance=example)
                    if isinstance(mapped_example, tuple):
                        mapped_example, mapped_tokens = mapped_example[0], mapped_example[1]
                        mapped_token_list.append(mapped_tokens) if mapped_tokens else None
                    nlu_ipa_mapped_example_list.append(mapped_example)

                if not mapped_token_list:
                    raise ZeroMappedTokensException()

                ipa_model = Word2VecModel(
                    model_name="ipa_model",
                    dataset=nlu_ipa_mapped_example_list,
                    epochs=self.epochs
                )

                # train
                ipa_model.train()
                for token, test_token in eval_tokens_dict.items():
                    mapped_token = self._map(token)

                    if isinstance(mapped_token, tuple):
                        mapped_token = mapped_token[0]

                    print(f"Token: {token}")
                    print(f"Mapped: {mapped_token}")
                    print(f"Target: {test_token}")
                    print(f"Similarity before Mapping (Token - Target): "
                          f"{nlu_model.cosine_similarity(instances=[token, test_token])}")
                    print(f"Similarity after Mapping (Mapped Token - Target): "
                          f"{ipa_model.cosine_similarity(instances=[mapped_token, test_token])}")
                    print("\n\n")
                exit("Exiting...")

            elif self.method == MappingMethod.RULE_BASED:
                raise NotImplementedError()  # TODO

                nlu_rules_mapped_example_list = list()
                for example in track(nlu_example_list, description="Mapping NLU to Rules:"):
                    mapped_example = self._map(instance=example)
                    if isinstance(mapped_example, tuple):
                        mapped_example = mapped_example[0]
                    nlu_rules_mapped_example_list.append(mapped_example)

                rule_based_model = Word2VecModel(
                    model_name="rule_based_model",
                    dataset=nlu_rules_mapped_example_list,
                    epochs=10
                )

                # train
                nlu_model.train()
                rule_based_model.train()

            else:
                InvalidEvaluationMethodException()
        else:
            raise InvalidEvaluationLevelException()

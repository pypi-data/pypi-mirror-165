import logging
import os.path
import time
from typing import List, Text, Optional

import gensim.models
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
from rich.progress import Progress

from seetm.shared.constants import DEFAULT_EMBEDDING_MODELS_PATH
from seetm.shared.exceptions.core import (
    Word2VecModelTrainingException,
    InvalidNumberOfTokensException, Word2VecModelNotFoundException,
)
from seetm.utils.io import get_timestamp_str
from seetm.utils.text_preprocessing import tokenize


logger = logging.getLogger(__name__)
gensim.models.word2vec.logger.level = 60
gensim.utils.logger.level = 60


class Word2VecModel:
    def __init__(self, dataset: List[Text], model_name: Text, epochs: int = 10):
        self.dataset = self._preprocess(dataset)
        self.name = model_name if model_name else get_timestamp_str()
        self.model = None
        self.vocabulary = list()
        self.epochs = epochs
        self.epoch_progress = EpochProgress(total_epochs=epochs, model_type=model_name)

    @staticmethod
    def _preprocess(dataset: List) -> List:
        preprocessed_dataset = [tokenize(str.lower(instance)) for instance in dataset]
        return preprocessed_dataset

    def train(self):
        try:
            self.model = Word2Vec(
                sentences=self.dataset,
                min_count=1,
                callbacks=[self.epoch_progress],
                epochs=self.epochs,
            )
            self.vocabulary = list(self.model.wv.key_to_index.keys())
        except Exception as e:
            raise Word2VecModelTrainingException(e)

    def persist(self):
        self.model.save(os.path.join(DEFAULT_EMBEDDING_MODELS_PATH, self.name + ".w2v"))

    def cosine_similarity(self, instances: List) -> float:
        if len(instances) != 2:
            raise InvalidNumberOfTokensException()

        if not self.model:
            raise Word2VecModelNotFoundException()

        if instances[0] not in self.vocabulary or instances[1] not in self.vocabulary:
            return 0.0

        model: Word2Vec = self.model
        return model.wv.n_similarity(ws1=instances[0].split(), ws2=instances[1].split())

    def similar_tokens(self, token: Text) -> List:
        if not self.model:
            raise Word2VecModelNotFoundException()

        model: Word2Vec = self.model
        return model.wv.most_similar(token)


class EpochProgress(CallbackAny2Vec):
    def __init__(self, total_epochs: int, model_type: Text):
        self.epoch = 0
        self.training_task = None
        self.total_epochs = total_epochs
        self.model_type = model_type
        self.progress = Progress(transient=True)
        self._initialize_progress()

    def _initialize_progress(self):
        # initializing model type
        if self.model_type == "nlu_model":
            self.model_type = "NLU"
        elif self.model_type == "ipa_model":
            self.model_type = "IPA"
        else:
            self.model_type = "Rule-based"

        # initializing progress
        self.training_task = self.progress.add_task(f"Training Word2Vec [{self.model_type}]", total=self.total_epochs)

    def on_epoch_end(self, model):
        self.epoch += 1
        with self.progress as progress:
            progress.update(self.training_task, advance=1)
            time.sleep(0.1)

        if self.epoch == self.total_epochs:
            logger.info(f"{self.model_type} Word2Vec model was successfully "
                        f"trained for a total of {self.total_epochs} epochs")

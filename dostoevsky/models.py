import os

from typing import List, Dict, Optional

from fasttext import load_model as load_fasttext_model

from dostoevsky.tokenization import BaseTokenizer
from dostoevsky.corpora import BaseCorpusContainer, RusentimentCorpus
from dostoevsky.data import DATA_BASE_PATH


class BaseModel:

    def __init__(
        self,
        tokenizer: BaseTokenizer,
        lemmatize: bool = True,
        model_path: Optional[str] = None,
        corpus: Optional[BaseCorpusContainer] = None,
    ):
        self.model_path = model_path
        self.tokenizer = tokenizer
        self.lemmatize = lemmatize
        self.corpus = corpus
        self.model = (
            self.get_compiled_model()
            if self.model_path
            else self.get_raw_model()
        )

    def get_compiled_model(self):
        raise NotImplementedError

    def preprocess_input(self, sentences: List[str]):
        raise NotImplementedError

    def predict(self, sentences: List[str]):
        raise NotImplementedError

    def get_raw_model(self):
        raise NotImplementedError


class FastTextSocialNetworkModel(BaseModel):
    '''
    FastText model trained on RuSentiment dataset.
    '''

    SENTENCE_LENGTH: Optional[int] = None

    MODEL_PATH: str = os.path.join(
        DATA_BASE_PATH,
        'models/fasttext-social-network-model.bin'
    )

    def __init__(
        self,
        tokenizer: BaseTokenizer,
        lemmatize: bool = False,
    ):
        super(FastTextSocialNetworkModel, self).__init__(
            tokenizer=tokenizer,
            lemmatize=lemmatize,
            model_path=self.MODEL_PATH,
            corpus=None
        )

    def get_compiled_model(self):
        return load_fasttext_model(self.MODEL_PATH)

    def preprocess_input(self, sentences: List[str]) -> List[str]:
        return [
            ' '.join(
                token for token, _ in self.tokenizer.split(
                    sentence, lemmatize=self.lemmatize
                )
            )
            for sentence in sentences
        ]

    def predict(self, sentences: List[str], k: int = -1) -> List[
        Dict[str, float]
    ]:
        X = self.preprocess_input(sentences)
        Y = (
            self.model.predict(sentence, k=k) for sentence in X
        )
        return [
            dict(zip(
                (label.replace('__label__', '') for label in labels),
                scores
            )) for labels, scores in Y
        ]


class FastTextToxicModel(FastTextSocialNetworkModel):
    '''
    FastText model trained on russian toxic comments dataset.
    '''

    SENTENCE_LENGTH: Optional[int] = None

    MODEL_PATH: str = os.path.join(
        DATA_BASE_PATH,
        'models/fasttext-toxic-model.bin'
    )


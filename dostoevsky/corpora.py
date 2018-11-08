import csv

from typing import Generator, Optional, List, Tuple

from sklearn.preprocessing import LabelBinarizer


from dostoevsky.tokenization import BaseTokenizer
from dostoevsky.word_vectors import BaseWordVectorsContainer


class BaseCorpusContainer:

    def get_prepared_data(self) -> Generator[Tuple[List[List[float]], List[int]], None, None]:
        raise NotImplementedError


class RusentimentCorpus(BaseCorpusContainer):

    CSV_DELIMITER: str = ','
    CSV_QUOTECHAR: str = '"'

    UNKNOWN_LABEL: str = 'unknown'

    LABELS: List[str] = [
        'positive',
        'negative',
        'neutral',
        'skip',
        'speech',
        UNKNOWN_LABEL,
    ]

    def __init__(
        self,
        data_path: Optional[str],
        tokenizer: BaseTokenizer,
        word_vectors_container: BaseWordVectorsContainer,
        lemmatize: bool = True,
    ):
        self.data_path = data_path
        self.tokenizer = tokenizer
        self.lemmatize = lemmatize
        self.word_vectors_container = word_vectors_container
        self.label_encoder = self.get_label_encoder()

    def get_label_encoder(self) -> LabelBinarizer:
        label_encoder = LabelBinarizer()
        return label_encoder.fit(self.LABELS)

    def get_prepared_data(self) -> Generator[Tuple[List[List[float]], List[int]], None, None]:
        if not self.data_path:
            raise ValueError('data_path is None')
        with open(self.data_path) as source:
            reader = csv.reader(
                source,
                delimiter=self.CSV_DELIMITER,
                quotechar=self.CSV_QUOTECHAR,
            )
            for i, (label, text) in enumerate(reader):
                if i == 0:  # skip headers
                    continue
                encoded_label, *_ = self.label_encoder.transform([label])
                tokens = self.tokenizer.split(text, lemmatize=self.lemmatize)
                word_vectors = self.word_vectors_container.get_word_vectors(tokens)
                if not any(vector.any() for vector in word_vectors):  # type: ignore
                    # FIXME: find better embeddings
                    encoded_label, *_ = self.label_encoder.transform([
                        self.UNKNOWN_LABEL
                    ])
                yield word_vectors, encoded_label

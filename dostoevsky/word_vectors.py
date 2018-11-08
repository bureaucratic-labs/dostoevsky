from typing import List, Tuple

from numpy import zeros
from gensim.models import KeyedVectors, FastText


class BaseWordVectorsContainer:
    '''
    Base interface for class, that returns vector representations of given words
    '''

    def __init__(self, model_path: str, dimension: int, append_pos: bool = True, **kwargs):
        self.model_path = model_path
        self.dimension = dimension
        self.append_pos = append_pos
        self.vectors = self.get_vectors(**kwargs)
        self.unknown_word_vector = self.get_unknown_word_vector()

    def get_unknown_word_vector(self) -> List[float]:
        return zeros(self.dimension)

    def get_vectors(self):
        raise NotImplementedError

    def get_word_vectors(self, tokens: List[Tuple[str, str]]) -> List[
        List[float]
    ]:
        return [
            self.vectors[f'{word}_{pos}'] if (
                f'{word}_{pos}' in self.vectors
            ) else self.unknown_word_vector for word, pos in tokens
        ] if self.append_pos else [
            self.vectors[word] if (
                word in self.vectors
            ) else self.unknown_word_vector for word, _ in tokens
        ]


class Word2VecContainer(BaseWordVectorsContainer):

    def get_vectors(self, **kwargs):
        model = KeyedVectors.load_word2vec_format(self.model_path, **kwargs)
        model.init_sims(replace=True)
        return model


class FastTextContainer(BaseWordVectorsContainer):

    def get_vectors(self, **kwargs):
        model = FastText.load(self.model_path, **kwargs)
        return model

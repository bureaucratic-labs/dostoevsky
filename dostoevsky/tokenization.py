from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

from razdel import tokenize as regex_tokenize


class BaseTokenizer(ABC):
    """
    Base tokenizer interface
    """

    @abstractmethod
    def split(self, text: str, lemmatize: bool = True) -> List[Tuple[str, Optional[str]]]:
        """
        Each subclass of BaseTokenizer must inplement this method
        Returns list with tuples like that one:
        [('приехать', 'VERB'), ('дом', 'NOUN')]
        """
        raise NotImplementedError


class RegexTokenizer(BaseTokenizer):
    """
    Tokenizer based on one of most accurate and fast tokenizers for russian
    language text - razdel. This tokenizer doesn't performs POS tagging
    and lemmatization.
    """

    def split(self, text: str, lemmatize: bool = False) -> List[Tuple[str, Optional[str]]]:
        return [(token.text.lower(), None) for token in regex_tokenize(text)]

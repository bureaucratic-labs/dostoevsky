from typing import List, Tuple, Set

from pymorphy2 import MorphAnalyzer
from b_labs_models import Tokenizer, POSTagger
from russian_tagsets import converters


opencorpora_to_ud_convert = converters.converter('opencorpora-int', 'ud14')


class BaseTokenizer:
    '''
    Base tokenizer interface
    '''

    def split(self, text: str, lemmatize: bool = True) -> List[
        Tuple[str, str]
    ]:
        '''
        Each subclass of BaseTokenizer must inplement this method
        Returns list with tuples like that one:
        [('приехать', 'VERB'), ('дом', 'NOUN')]
        '''
        raise NotImplementedError


class BaselineTokenizer(BaseTokenizer):
    '''
    Simple tokenizer that uses pre-trained CRF model from B-Labs and
    takes first form of each word from pymorphy2 output
    '''

    POS_WITHOUT_NORMAL_FORM: Set[str] = {
        'SYMB',
        'NUMB',
        'PNCT',
        'LATN'
    }

    def __init__(self):
        self.tokenizer = Tokenizer()
        self.tagger = POSTagger()
        self.morph = MorphAnalyzer()

    def get_token_text(self, token: str, pos: str, lemmatize: bool = False):

        if pos in self.POS_WITHOUT_NORMAL_FORM or not lemmatize:
            return token.lower()

        text: str = token
        forms: List[Tuple[str, str, str]] = [
            (form.word, form.normal_form, form.tag)
            for form in self.morph.parse(token)
        ]
        for (word, normal_form, tag) in forms:
            if pos in tag:
                text = normal_form
                break
        return text.lower()

    def split(self, text: str, lemmatize: bool = False):
        tokens: List[str] = list(self.tokenizer.split(text))
        parts_of_speech: List[str] = list(self.tagger.tag(tokens))
        return [
            (self.get_token_text(token, pos, lemmatize), pos)
            for token, pos in zip(tokens, parts_of_speech)
        ]


class UDBaselineTokenizer(BaselineTokenizer):
    '''
    Tokenizer that works similar to baseline tokenizer, but also
    converts OpenCorpora part of speech tags to Universal Dependencies
    format, because some word vectors (notably, RusVectores) was trained on UD tagset
    '''

    UNKNOWN_POS_TAG: str = 'X'

    def split(self, text: str, lemmatize: bool = False):
        tokens: List[Tuple[str, str]] = (
            super(UDBaselineTokenizer, self)
            .split(text=text, lemmatize=lemmatize)
        )
        results: List[Tuple[str, str]] = [
            (token, opencorpora_to_ud_convert(pos).split(' ')[0])
            if pos else (token, self.UNKNOWN_POS_TAG) for token, pos in tokens
        ]
        return results

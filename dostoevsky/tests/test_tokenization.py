from typing import List, Tuple


def test_baseline_tokenizer_simple_case(baseline_tokenizer):
    tokens: List[
        Tuple[str, str]
    ] = baseline_tokenizer.split('он приехал домой')
    assert tokens == [
        ('он', 'NPRO'),
        ('приехал', 'VERB'),
        ('домой', 'ADVB'),
    ]


def test_baseline_tokenizer_with_lemmatization(baseline_tokenizer):
    tokens: List[
        Tuple[str, str]
    ] = baseline_tokenizer.split('он приехал домой', lemmatize=True)
    assert tokens == [
        ('он', 'NPRO'),
        ('приехать', 'VERB'),
        ('домой', 'ADVB'),
    ]


def test_baseline_tokenizer_with_lemmatization_and_mixed_case_text(baseline_tokenizer):
    tokens: List[
        Tuple[str, str]
    ] = baseline_tokenizer.split('оН пРиехал доМой', lemmatize=True)
    assert tokens == [
        ('он', 'NPRO'),
        ('приехать', 'VERB'),
        ('домой', 'ADVB'),
    ]


def test_ud_baseline_tokenizer_simple_case(ud_baseline_tokenizer):
    tokens: List[
        Tuple[str, str]
    ] = ud_baseline_tokenizer.split('она была очень красивой')
    assert tokens == [
        ('она', 'PRON'),
        ('была', 'VERB'),
        ('очень', 'ADV'),
        ('красивой', 'ADJ'),
    ]


def test_ud_baseline_tokenizer_with_special_words(ud_baseline_tokenizer):
    tokens: List[
        Tuple[str, str]
    ] = ud_baseline_tokenizer.split('123, test')
    assert tokens == [
        ('123', 'NUM'),
        (',', 'PUNCT'),
        ('test', 'X'),
    ]


def test_ud_baseline_tokenizer_with_unknown_word(ud_baseline_tokenizer):
    tokens: List[
        Tuple[str, str]
    ] = ud_baseline_tokenizer.split('asdasdasde21e')
    assert tokens == [
        ('asdasdasde21e', 'X'),
    ]

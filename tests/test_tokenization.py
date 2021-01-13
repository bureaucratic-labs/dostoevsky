from typing import List, Optional, Tuple


def test_regex_tokenizer_base_case(regex_tokenizer):
    tokens: List[
        Tuple[str, Optional[str]]
    ] = regex_tokenizer.split('он приехал домой')
    assert tokens == [
        ('он', None),
        ('приехал', None),
        ('домой', None),
    ]


def test_regex_tokenizer_lower_case(regex_tokenizer):
    tokens: List[
        Tuple[str, Optional[str]]
    ] = regex_tokenizer.split('оН пРиехал доМой')
    assert tokens == [
        ('он', None),
        ('приехал', None),
        ('домой', None),
    ]

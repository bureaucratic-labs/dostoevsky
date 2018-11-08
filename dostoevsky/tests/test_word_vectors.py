from typing import List, Tuple


def test_word_vectors_simple_case(
    ud_baseline_tokenizer,
    word_vectors_dimension,
    word_vectors_container
):
    tokens: List[
        Tuple[str, str]
    ] = ud_baseline_tokenizer.split('она была очень красивой', lemmatize=True)
    vectors = word_vectors_container.get_word_vectors(tokens)
    assert len(tokens) == len(vectors)
    assert all(vector.shape[0] == word_vectors_dimension for vector in vectors)


def test_word_vectors_with_unknown_words(
    ud_baseline_tokenizer,
    word_vectors_dimension,
    word_vectors_container
):
    tokens: List[
        Tuple[str, str]
    ] = ud_baseline_tokenizer.split('крутое видео', lemmatize=False)
    vectors = word_vectors_container.get_word_vectors(tokens)
    assert len(tokens) == len(vectors)
    assert not all(vectors[0])  # unknown word, vector filled with zeros
    assert all(vectors[1])  # known word
    assert vectors[0].shape[0] == vectors[1].shape[0] == word_vectors_dimension

from keras.preprocessing.sequence import pad_sequences


def test_rusentiment_corpus_get_prepared_data(
    rusentiment_corpus,
    word_vectors_container,
):
    X_train, y_train = [], []
    for i, (vectors, label) in enumerate(
        rusentiment_corpus.get_prepared_data()
    ):
        X_train.append(vectors)
        y_train.append(label)
        if i >= 9:
            break
    assert len(X_train) == len(y_train)
    assert pad_sequences(X_train, maxlen=60).shape == (
        10, 60, word_vectors_container.dimension
    )

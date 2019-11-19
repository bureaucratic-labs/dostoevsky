def test_rusentiment_corpus_get_prepared_data(
    rusentiment_corpus,
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
    assert X_train[0]

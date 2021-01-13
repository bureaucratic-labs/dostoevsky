def test_rusentiment_corpus_get_data(
    rusentiment_corpus,
):
    X_train, y_train = [], []
    for i, (text, label) in enumerate(
        rusentiment_corpus.get_data()
    ):
        X_train.append(text)
        y_train.append(label)
        if i >= 9:
            break
    assert len(X_train) == len(y_train)
    assert X_train[0]

import os

from typing import List, Optional

from keras.models import Model, load_model
from keras.layers import Input, Dense, concatenate, Activation, Dropout
from keras.layers.convolutional import Conv1D
from keras.layers.pooling import GlobalMaxPooling1D
from keras.preprocessing.sequence import pad_sequences

from dostoevsky.tokenization import BaseTokenizer
from dostoevsky.word_vectors import BaseWordVectorsContainer
from dostoevsky.corpora import BaseCorpusContainer, RusentimentCorpus
from dostoevsky.data import DATA_BASE_PATH


class BaseModel:

    def __init__(
        self,
        sentence_length: int,
        tokenizer: BaseTokenizer,
        word_vectors_container: BaseWordVectorsContainer,
        lemmatize: bool = True,
        model_path: Optional[str] = None,
        corpus: Optional[BaseCorpusContainer] = None,
    ):
        self.model_path = model_path
        self.sentence_length = sentence_length
        self.tokenizer = tokenizer
        self.word_vectors_container = word_vectors_container
        self.lemmatize = lemmatize
        self.corpus = corpus
        self.model = (
            self.get_compiled_model()
            if self.model_path
            else self.get_raw_model()
        )

    def get_compiled_model(self):
        return load_model(self.model_path)

    def predict(self, sentences: List[str]) -> List[str]:
        X = pad_sequences([
            self.word_vectors_container.get_word_vectors(
                self.tokenizer.split(sentence, lemmatize=self.lemmatize)
            ) for sentence in sentences
        ], maxlen=self.sentence_length, dtype='float32')
        Y = self.model.predict(X)
        labels: List[str] = (
            self
            .corpus
            .label_encoder
            .inverse_transform(Y)
        )
        return labels

    def get_raw_model(self):
        raise NotImplementedError


class BaseCNNModel(BaseModel):
    '''
    Slightly modified word-level CNN model from https://github.com/sismetanin/sentiment-analysis-of-tweets-in-russian
    '''

    def get_raw_model(self):
        branches = []
        tweet_input = Input(shape=(
            self.sentence_length,
            self.word_vectors_container.dimension
        ), dtype='float32')
        x = Dropout(0.2)(tweet_input)

        for size, filters_count in [(2, 10), (3, 10), (4, 10), (5, 10)]:
            for i in range(filters_count):
                branch = Conv1D(
                    filters=1,
                    kernel_size=size,
                    padding='valid',
                    activation='relu'
                )(x)
                branch = GlobalMaxPooling1D()(branch)
                branches.append(branch)

        x = concatenate(branches, axis=1)
        x = Dropout(0.2)(x)
        x = Dense(30, activation='relu')(x)
        x = Dense(len(self.corpus.label_encoder.classes_))(x)
        output = Activation('softmax')(x)

        model = Model(inputs=[tweet_input], outputs=[output])
        model.compile(
            loss='categorical_crossentropy',
            optimizer='rmsprop',
            metrics=['categorical_accuracy']
        )
        return model


class SocialNetworkModel(BaseCNNModel):
    '''
    Trained on RuSentiment dataset (https://github.com/text-machine-lab/rusentiment)
    Achieves up to ~0.70 F1 (original RuSentiment model has ~0.72 F1 score)
    '''

    SENTENCE_LENGTH: int = 60
    MODEL_PATH: str = os.path.join(
        DATA_BASE_PATH,
        'models/cnn-social-network-model.hdf5'
    )

    def __init__(
        self,
        tokenizer: BaseTokenizer,
        word_vectors_container: BaseWordVectorsContainer,
        lemmatize: bool = False,
    ):
        super(SocialNetworkModel, self).__init__(
            sentence_length=self.SENTENCE_LENGTH,
            tokenizer=tokenizer,
            word_vectors_container=word_vectors_container,
            lemmatize=lemmatize,
            model_path=self.MODEL_PATH,
            corpus=RusentimentCorpus(
                data_path=None,
                tokenizer=tokenizer,
                word_vectors_container=word_vectors_container,
                lemmatize=lemmatize,
            )
        )

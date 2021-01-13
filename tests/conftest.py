import os

import pytest

from dostoevsky.corpora import RusentimentCorpus
from dostoevsky.data import DATA_BASE_PATH, DataDownloader
from dostoevsky.tokenization import RegexTokenizer


@pytest.fixture(scope='session')
def regex_tokenizer():
    return RegexTokenizer()


@pytest.fixture(scope='session')
def data_downloader():
    return DataDownloader()


@pytest.fixture(scope='session')
def embeddings_path(data_downloader) -> str:
    filesize: int = data_downloader.download(
        'embeddings/vk-min-100-300d-none-limited.tar.xz',
        'embeddings/vk-min-100-300d-none-limited.tar.xz',
    )
    assert filesize > 0
    return os.path.join(
        DATA_BASE_PATH,
        'embeddings/vk-min-100-300d-none-limited.vec',
    )


@pytest.fixture(scope='session')
def rusentiment_corpus_data(data_downloader):
    filesize: int = data_downloader.download(
        'corpora/rusentiment.tar.xz',
        'corpora/rusentiment',
    )
    assert filesize > 0
    return os.path.join(
        DATA_BASE_PATH,
        'corpora/',
    )


@pytest.fixture(scope='session')
def rusentiment_corpus_path(rusentiment_corpus_data):
    return os.path.join(rusentiment_corpus_data, 'rusentiment_random_posts.csv')


@pytest.fixture(scope='session')
def rusentiment_test_corpus_path(rusentiment_corpus_data):
    return os.path.join(rusentiment_corpus_data, 'rusentiment_test.csv')


@pytest.fixture(scope='session')
def rusentiment_corpus(
    rusentiment_corpus_path,
):
    return RusentimentCorpus(
        data_path=rusentiment_corpus_path,
    )


@pytest.fixture(scope='session')
def rusentiment_test_corpus(
    rusentiment_test_corpus_path,
):
    return RusentimentCorpus(
        data_path=rusentiment_test_corpus_path,
    )

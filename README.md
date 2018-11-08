# Dostoevsky [![Build Status](https://travis-ci.org/bureaucratic-labs/dostoevsky.svg?branch=master)](https://travis-ci.org/bureaucratic-labs/dostoevsky)
Library for sentiment analysis of russian language

Currently, contains only one model: for classification of social networks comments / text messengers messages

## Install

```bash
$ pip install dostoevsky
```

## Social networks comment model

This model was trained on [RuSentiment dataset](https://github.com/text-machine-lab/rusentiment) and achieves up to ~0.70 F1 score  
![](https://i.imgur.com/bGAEWvg.png)

### Usage

First of all, you'll need to download pretrained word embeddings and model:

```bash
$ python -m doestoevsky.data download vk-embeddings cnn-social-network-model
```

Then, we can build our pipeline: `text -> tokenizer -> word embeddings -> CNN`

```python
from dostoevsky.tokenization import UDBaselineTokenizer
from dostoevsky.word_vectors import Word2VecContainer
from dostoevsky.corpora import RusentimentCorpus
from dostoevsky.data import VK_WORD_VECTORES_PATH, VK_WORD_VECTORES_DIMENSION
from dostoevsky.models import SocialNetworkModel

tokenizer = UDBaselineTokenizer()
tokenizer.split('всё очень плохо')  # [('всё', 'ADJ'), ('очень', 'ADV'), ('плохо', 'ADV')]

word_vectors_container = Word2VecContainer(
  model_path=VK_WORD_VECTORES_PATH,
  dimension=VK_WORD_VECTORES_DIMENSION,
  append_pos=False,  # our embeddings doesn't have an POS suffix (like RusVectores have)
)

vectors = word_vectors.get_word_vectors(tokens)
vectors.shape  # (3, 300) - three words/vectors with dim=300

model = SocialNetworkModel(
  tokenizer=tokenizer,
  word_vectors_container=word_vectors_container,
  lemmatize=False,
)

model.predict(['наступили на ногу', 'всё суперски'])  # array(['negative', 'positive'], dtype='<U8')

```

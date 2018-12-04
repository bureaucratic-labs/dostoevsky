# Dostoevsky [![Build Status](https://travis-ci.org/bureaucratic-labs/dostoevsky.svg?branch=master)](https://travis-ci.org/bureaucratic-labs/dostoevsky)

<img align="right" src="https://i.imgur.com/uLMWPuL.png">

Library for sentiment analysis of russian language

Currently, contains only one model: for classification of social networks comments / text messengers messages

## Install

Please note that `Dostoevsky` supports only Python 3.6 (3.7+ version'll be supported when tensorflow get it support, sorry)

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
from dostoevsky.word_vectors import SocialNetworkWordVectores
from dostoevsky.models import SocialNetworkModel

tokenizer = UDBaselineTokenizer()
tokens = tokenizer.split('всё очень плохо')  # [('всё', 'ADJ'), ('очень', 'ADV'), ('плохо', 'ADV')]

word_vectors_container = SocialNetworkWordVectores()

vectors = word_vectors_container.get_word_vectors(tokens)
vectors.shape  # (3, 300) - three words/vectors with dim=300

model = SocialNetworkModel(
  tokenizer=tokenizer,
  word_vectors_container=word_vectors_container,
  lemmatize=False,
)

model.predict(['наступили на ногу', 'всё суперски'])  # array(['negative', 'positive'], dtype='<U8')

```

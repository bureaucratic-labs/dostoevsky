# Dostoevsky [![Build Status](https://travis-ci.org/bureaucratic-labs/dostoevsky.svg?branch=master)](https://travis-ci.org/bureaucratic-labs/dostoevsky) [![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fbureaucratic-labs%2Fdostoevsky.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fbureaucratic-labs%2Fdostoevsky?ref=badge_shield)

<img align="right" src="https://i.imgur.com/uLMWPuL.png">

Sentiment analysis library for russian language

## Install

Please note that `Dostoevsky` supports only Python 3.6+

```bash
$ pip install dostoevsky
```

## Social network model [FastText]

This model was trained on [RuSentiment dataset](https://github.com/text-machine-lab/rusentiment) and achieves up to ~0.71 F1 score.  
Hyperparameters used for training:
```
epoch = 10
lr = 0.21909
dim = 64
minCount = 1
wordNgrams = 3
minn = 2
maxn = 5
bucket = 259929
dsub = 2
loss = one-vs-all
```

### Usage

First of all, you'll need to download binary model:

```bash
$ dostoevsky download fasttext-social-network-model
```

Then you can use sentiment analyzer:

```python
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

tokenizer = RegexTokenizer()
tokens = tokenizer.split('всё очень плохо')  # [('всё', None), ('очень', None), ('плохо', None)]

model = FastTextSocialNetworkModel(tokenizer=tokenizer)

messages = [
    'привет',
    'я люблю тебя!!',
    'малолетние дебилы'
]

results = model.predict(messages, k=2)

for message, sentiment in zip(messages, results):
    """
    привет -> {'speech': 1.0000100135803223, 'skip': 0.0020607432816177607}
    я люблю тебя!! -> {'positive': 0.9886782765388489, 'skip': 0.005394937004894018}
    малолетние дебилы -> {'negative': 0.9525841474533081, 'neutral': 0.13661839067935944}]
    """
    print(message, '->', sentiment)
```

## Social network model [CNN]

This model was trained on RuSentiment dataset too, but uses pretrained embeddings from RuSentiment dataset and achieves up to ~0.70 F1 score. Also, this model is implemented using Keras, so its possible to run on GPU.  
![](https://i.imgur.com/bGAEWvg.png)

### Usage

First of all, you'll need to download pretrained word embeddings and model:

```bash
$ dostoevsky download vk-embeddings cnn-social-network-model
```

Then, we can build our pipeline: `text -> tokenizer -> word embeddings -> CNN`

```python
from dostoevsky.tokenization import UDBaselineTokenizer, RegexTokenizer
from dostoevsky.embeddings import SocialNetworkEmbeddings
from dostoevsky.models import SocialNetworkModel

tokenizer = UDBaselineTokenizer() or RegexTokenizer()
tokens = tokenizer.split('всё очень плохо')  # [('всё', 'ADJ'), ('очень', 'ADV'), ('плохо', 'ADV')]

embeddings_container = SocialNetworkEmbeddings()

vectors = embeddings_container.get_word_vectors(tokens)
vectors.shape  # (3, 300) - three words/vectors with dim=300

model = SocialNetworkModel(
  tokenizer=tokenizer,
  embeddings_container=embeddings_container,
  lemmatize=False,
)

messages = [
    'наступили на ногу',
    'всё суперски',
]

results = model.predict(messages)

for message, sentiment in zip(messages, results):
    print(message, '->', sentiment)  # наступили на ногу -> negative
```


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fbureaucratic-labs%2Fdostoevsky.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fbureaucratic-labs%2Fdostoevsky?ref=badge_large)

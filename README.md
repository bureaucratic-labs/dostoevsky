# Dostoevsky ![Test & Lint](https://github.com/bureaucratic-labs/dostoevsky/workflows/Test%20&%20Lint/badge.svg?branch=master)

Sentiment analysis library for russian language

## Install

Please note that `Dostoevsky` supports only Python 3.7+ on both Linux and Windows

```bash
$ pip install dostoevsky
```

## Social network model [FastText]

This model was trained on [RuSentiment dataset](https://github.com/text-machine-lab/rusentiment) and achieves up to ~0.71 F1 score.  

### Usage

First of all, you'll need to download binary model:

```bash
$ python -m dostoevsky download fasttext-social-network-model
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
    # привет -> {'speech': 1.0000100135803223, 'skip': 0.0020607432816177607}
    # люблю тебя!! -> {'positive': 0.9886782765388489, 'skip': 0.005394937004894018}
    # малолетние дебилы -> {'negative': 0.9525841474533081, 'neutral': 0.13661839067935944}]
    print(message, '->', sentiment)
```

## Articles

* 🇷🇺 [Dostoevsky — анализ тональности в Python за 5 минут](https://egorovegor.ru/analiz-tonalnosti-s-python-i-dostoevsky/)
* 🇷🇺 [Семантический анализ мнений о поправках к Конституции на основе данных ВКонтакте ](https://leftjoin.ru/all/constitution-sentiment-analysis/)
* 🇷🇺 [Как писать посты в стиле Артемия Лебедева? Подробный анализ телеграм-канала и кое-что еще](https://habr.com/ru/post/596035/)

Feel free to extend this list with your article! ✨

## Related projects

* [David Dale](https://github.com/avidale) BERT-based models for [emotion detection](https://huggingface.co/cointegrated/rubert-tiny2-cedr-emotion-detection?text=%D0%93%D1%80%D1%83%D1%81%D1%82%D1%8C-%D1%82%D0%BE%D1%81%D0%BA%D0%B0+%D0%BC%D0%B5%D0%BD%D1%8F+%D1%81%D1%8A%D0%B5%D0%B4%D0%B0%D0%B5%D1%82) and [classification of toxicity](https://huggingface.co/cointegrated/rubert-tiny-toxicity)

## Citation

If you use the library in a research project, please include the following citation for the RuSentiment data:
```
@inproceedings{rogers-etal-2018-rusentiment,
    title = "{R}u{S}entiment: An Enriched Sentiment Analysis Dataset for Social Media in {R}ussian",
    author = "Rogers, Anna  and
      Romanov, Alexey  and
      Rumshisky, Anna  and
      Volkova, Svitlana  and
      Gronas, Mikhail  and
      Gribov, Alex",
    booktitle = "Proceedings of the 27th International Conference on Computational Linguistics",
    month = aug,
    year = "2018",
    address = "Santa Fe, New Mexico, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/C18-1064",
    pages = "755--763",
}

```

from setuptools import (
    setup,
    find_packages,
)


def get_long_description() -> str:
    with open('README.md', encoding='utf-8') as source:
        return source.read()


setup(
    name='dostoevsky',
    version='0.5.0',
    description='Sentiment analysis library for russian language',
    url='https://github.com/bureaucratic-labs/dostoevsky',
    author='Bureaucratic Labs',
    author_email='hello@b-labs.pro',
    license='MIT',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='natural language processing, sentiment analysis',
    packages=find_packages(),
    package_data={
        'dostoevsky': [
            'data/corpora/*',
            'data/embeddings/*',
            'data/models/*',
        ]
    },
    scripts=['bin/dostoevsky'],
    install_requires=[
        'b-labs-models==2017.8.22',
        'razdel==0.4.0',
        'fasttext==0.9.1',
        'pymorphy2==0.8',
        'pytest==5.3.5',
        'russian-tagsets==0.6',
        'scikit-learn==0.22.1',
    ],
)

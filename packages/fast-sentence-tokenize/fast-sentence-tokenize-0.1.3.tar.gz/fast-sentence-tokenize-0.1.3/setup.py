# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_sentence_tokenize',
 'fast_sentence_tokenize.bp',
 'fast_sentence_tokenize.datablock',
 'fast_sentence_tokenize.datablock.dto',
 'fast_sentence_tokenize.datablock.wordnet',
 'fast_sentence_tokenize.dmo',
 'fast_sentence_tokenize.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock', 'nltk', 'spacy==3.3']

setup_kwargs = {
    'name': 'fast-sentence-tokenize',
    'version': '0.1.3',
    'description': 'Fast and Efficient Sentence Tokenization',
    'long_description': None,
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.5',
}


setup(**setup_kwargs)

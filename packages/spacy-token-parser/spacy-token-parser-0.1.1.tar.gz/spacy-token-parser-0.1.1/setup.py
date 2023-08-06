# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacy_token_parser', 'spacy_token_parser.dmo', 'spacy_token_parser.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock', 'spacy==3.3', 'wordnet-lookup']

setup_kwargs = {
    'name': 'spacy-token-parser',
    'version': '0.1.1',
    'description': 'Use spaCy to Parse Input Tokens',
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

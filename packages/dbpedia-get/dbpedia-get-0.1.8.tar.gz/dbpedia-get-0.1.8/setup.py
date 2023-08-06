# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbpedia_get',
 'dbpedia_get.lookup',
 'dbpedia_get.lookup.bp',
 'dbpedia_get.lookup.dmo',
 'dbpedia_get.lookup.dto',
 'dbpedia_get.lookup.svc',
 'dbpedia_get.recipes',
 'dbpedia_get.transform',
 'dbpedia_get.transform.bp',
 'dbpedia_get.transform.dmo',
 'dbpedia_get.transform.svc']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode',
 'baseblock',
 'datasets>=2.4.0,<3.0.0',
 'fast_sentence_segment',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.2.3,<2.0.0',
 'spacy==3.3',
 'tabulate',
 'unicodedata2',
 'unidecode',
 'wikipedia>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'dbpedia-get',
    'version': '0.1.8',
    'description': 'dbPedia Concept Linking and Redirect Analysis',
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

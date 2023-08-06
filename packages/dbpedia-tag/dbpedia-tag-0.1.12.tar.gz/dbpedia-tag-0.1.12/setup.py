# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbpedia_tag',
 'dbpedia_tag.bp',
 'dbpedia_tag.dmo',
 'dbpedia_tag.dto',
 'dbpedia_tag.recipes',
 'dbpedia_tag.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock', 'dbpedia-ent', 'fast-sentence-tokenize']

setup_kwargs = {
    'name': 'dbpedia-tag',
    'version': '0.1.12',
    'description': 'Perform runtime tagging and annotation of unstructured text',
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

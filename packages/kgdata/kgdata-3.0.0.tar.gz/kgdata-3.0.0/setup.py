# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kgdata',
 'kgdata.dbpedia',
 'kgdata.misc',
 'kgdata.wikidata',
 'kgdata.wikidata.datasets',
 'kgdata.wikidata.models',
 'kgdata.wikipedia',
 'kgdata.wikipedia.datasets',
 'kgdata.wikipedia.models']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'chardet>=4.0.0,<5.0.0',
 'cityhash>=0.2.3,<0.3.0',
 'click>=8.1.3,<9.0.0',
 'fastnumbers>=3.1.0,<4.0.0',
 'hugedict>=2.4.2,<3.0.0',
 'loguru>=0.6.0',
 'lxml>=4.9.0,<5.0.0',
 'numpy>=1.22.3,<2.0.0',
 'orjson>=3.6.8,<4.0.0',
 'parsimonious>=0.8.1,<0.9.0',
 'pyserini>=0.17.0,<0.18.0',
 'pyspark==3.3.0',
 'rdflib>=6.1.1,<7.0.0',
 'redis>=3.5.3,<4.0.0',
 'requests>=2.28.0,<3.0.0',
 'rsoup>=2.5.1,<3.0.0',
 'ruamel.yaml>=0.17.9,<0.18.0',
 'sem-desc>=3.5.2,<4.0.0',
 'six>=1.16.0,<2.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'ujson>=5.1.0,<6.0.0']

setup_kwargs = {
    'name': 'kgdata',
    'version': '3.0.0',
    'description': 'Library to process dumps of knowledge graphs (Wikipedia, DBpedia, Wikidata)',
    'long_description': '# kgdata ![PyPI](https://img.shields.io/pypi/v/kgdata) ![Documentation](https://readthedocs.org/projects/kgdata/badge/?version=latest&style=flat)\n\nKGData is a library to process dumps of Wikipedia, Wikidata. What it can do:\n\n- Clean up the dumps to ensure the data is consistent (resolve redirect, remove dangling references)\n- Create embedded key-value databases to access entities from the dumps.\n- Extract Wikidata ontology.\n- Extract Wikipedia tables and convert the hyperlinks to Wikidata entities.\n- Create Pyserini indices to search Wikidata’s entities.\n- and more\n\nFor a full documentation, please see[the website](https://kgdata.readthedocs.io/).\n\n## Installation\n\nFrom PyPI (using pre-built binaries):\n\n```bash\npip install kgdata\n```\n',
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/binh-vu/kgdata',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

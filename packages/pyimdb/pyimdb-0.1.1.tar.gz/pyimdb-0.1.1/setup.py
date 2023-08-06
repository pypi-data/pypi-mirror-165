# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyimdb']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pyimdb',
    'version': '0.1.1',
    'description': 'A wrapper python for imdb.com',
    'long_description': "# Python IMDB\n\n[![Python package](https://github.com/hudsonbrendon/pyimdb/actions/workflows/python-package.yml/badge.svg)](https://github.com/hudsonbrendon/pyimdb/actions/workflows/python-package.yml)\n[![Github Issues](http://img.shields.io/github/issues/hudsonbrendon/pyimdb.svg?style=flat)](https://github.com/hudsonbrendon/pyimdb/issues?sort=updated&state=open)\n![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)\n\nA wrapper python for imdb.com\n\n# Quick start\n\n```bash\n$ pip install pyimdb\n```\n\n# Usage\n\nWith your key in hand, it's time to authenticate, so run:\n\n```python\n>>> from pyimdb import IMDB\n\n>>> imdb = IMDB()\n```\n\n# Popular TV Shows\n\nReturns list of popular tv shows.\n\n```python\n>>> imdb.popular_tv_shows()\n```\nor\n\n```python\n>>> imdb.popular_tv_shows(limit=10)\n```\n\n# Popular Movies\n\nReturns list of popular movies.\n\n```python\n>>> imdb.popular_movies()\n```\nor\n\n```python\n>>> imdb.popular_movies(limit=10)\n```\n\n# TOP Rated TV Shows\n\nReturns list of top rated tv shows.\n\n```python\n>>> imdb.top_rated_tv_shows()\n```\nor\n\n```python\n>>> imdb.top_rated_tv_shows(limit=2)\n```\n\n# TOP Rated Movies\n\nReturns list of top rated movies.\n\n```python\n>>> imdb.top_rated_movies()\n```\nor\n\n```python\n>>> imdb.top_rated_movies(limit=2)\n```\n\n# Dependencies\n\n- Python >=3.8\n\n# License\n\n[MIT](http://en.wikipedia.org/wiki/MIT_License)\n",
    'author': 'Hudson Brendon',
    'author_email': 'contato.hudsonbrendon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hudsonbrendon/python-imdb#readme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

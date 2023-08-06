# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cacheframe']

package_data = \
{'': ['*']}

install_requires = \
['pandas']

setup_kwargs = {
    'name': 'cacheframe',
    'version': '0.1.1',
    'description': 'Dataframe caches.',
    'long_description': None,
    'author': 'Yevgnen Koh',
    'author_email': 'wherejoystarts@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mytweets', 'mytweets.api']

package_data = \
{'': ['*']}

install_requires = \
['oauthlib>=3.2.0,<4.0.0', 'requests-oauthlib>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'mytweets',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'yrcmpbll',
    'author_email': 'yuri.campbell@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

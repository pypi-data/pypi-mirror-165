# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vivi']

package_data = \
{'': ['*']}

install_requires = \
['starlette>=0.20.4,<0.21.0']

setup_kwargs = {
    'name': 'vivi',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Daan van der Kallen',
    'author_email': 'mail@daanvdk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

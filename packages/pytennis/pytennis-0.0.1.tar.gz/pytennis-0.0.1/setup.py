# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytennis', 'pytennis.data']

package_data = \
{'': ['*']}

install_requires = \
['fastdownload>=0.0.7,<0.0.8', 'portray>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'pytennis',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Robert Seidl',
    'author_email': 'robertseidl425@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)

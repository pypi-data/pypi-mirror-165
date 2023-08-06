# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['likeprocessing']

package_data = \
{'': ['*']}

install_requires = \
['pygame>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'likeprocessing',
    'version': '0.1.4.1',
    'description': 'Like processing library with pygame',
    'long_description': None,
    'author': 'Pierre Lemaitre',
    'author_email': 'oultetman@sfr.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

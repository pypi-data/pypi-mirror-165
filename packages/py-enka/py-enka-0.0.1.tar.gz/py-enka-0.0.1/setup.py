# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['enka', 'enka.model']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'pydantic>=1.9.2,<2.0.0']

setup_kwargs = {
    'name': 'py-enka',
    'version': '0.0.1',
    'description': '',
    'long_description': '# Py-Enka\n\n用于 Python 的 [Enka.Network](https://enka.network) API',
    'author': 'Arko',
    'author_email': 'arko.space.cc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ArkoClub/py-enka',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seaportpy', 'seaportpy.abi', 'seaportpy.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0', 'web3>=5.27.0,<6.0.0']

setup_kwargs = {
    'name': 'seaportpy',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'OpenSea Developers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

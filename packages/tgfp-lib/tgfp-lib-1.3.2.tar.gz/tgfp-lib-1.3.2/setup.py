# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tgfp_lib']

package_data = \
{'': ['*']}

install_requires = \
['pymongo>=4.2.0,<5.0.0', 'pytz>=2022.2.1,<2023.0.0']

setup_kwargs = {
    'name': 'tgfp-lib',
    'version': '1.3.2',
    'description': 'The Great Football Pool Project',
    'long_description': None,
    'author': 'John Sturgeon',
    'author_email': 'john.sturgeon@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

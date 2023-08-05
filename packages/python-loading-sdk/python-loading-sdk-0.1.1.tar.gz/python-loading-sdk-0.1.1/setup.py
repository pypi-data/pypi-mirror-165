# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loading_sdk', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'python-loading-sdk',
    'version': '0.1.1',
    'description': 'Python api wrapper for loading.se',
    'long_description': None,
    'author': 'hnrkcode',
    'author_email': '44243358+hnrkcode@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

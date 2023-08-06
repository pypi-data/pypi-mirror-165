# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commonmodel']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1', 'pydantic>=1.8.1']

setup_kwargs = {
    'name': 'common-model',
    'version': '0.5.1',
    'description': 'Universal Data Schemas',
    'long_description': None,
    'author': 'Ken Van Haren',
    'author_email': 'kenvanharen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpleapi']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.2,<2.0.0']

setup_kwargs = {
    'name': 'simplestapi',
    'version': '0.1.0',
    'description': 'SimpleAPI is a minimalistic, unopinionated web framework for Python, inspired by FastAPI & Flask',
    'long_description': None,
    'author': 'Adham Salama',
    'author_email': 'adham.salama@zohomail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adhamsalama/simpleapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

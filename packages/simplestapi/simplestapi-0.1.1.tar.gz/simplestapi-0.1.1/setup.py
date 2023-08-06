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
    'version': '0.1.1',
    'description': 'SimpleAPI is a minimalistic, unopinionated web framework for Python, inspired by FastAPI & Flask',
    'long_description': '# SimpleAPI\n\n![banner](https://i.imgur.com/Q3kFiKf.png)\nSimpleAPI is a minimalistic, unopinionated web framework for Python, inspired by FastAPI & Flask.\n\nSimpleAPI is a WSGI compliant framework.\n\nThis is a hobby project made for educational purposes because I want to try learning writing a web server framework.\n\nSo, this is obviously not meant for production environments.\n\nDevelopment of SimpleAPI is tracked at [this](https://github.com/users/adhamsalama/projects/1) GitHub project.\n\n## Installation\n\n`pip install simplestapi`\n\n## Usage\n\nAn example of using SimpleAPI:\n\nCopy the following code to a file called `app.py`\n\n```python\nfrom simpleapi import SimpleAPI\n\napp = SimpleAPI()\n\n@app.get("/hello")\ndef hello():\n    return "Hello, world!"\n```\n\nRun it with `gunicorn app:app`\n\nMore examples can be found in [tests](./tests)\n\n## Documentation\n\n[https://adhamsalama.github.io/simpleapi](https://adhamsalama.github.io/simpleapi)\n',
    'author': 'Adham Salama',
    'author_email': 'adham.salama@zohomail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://adhamsalama.github.io/simpleapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

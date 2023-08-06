# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['little_server', 'little_server.utils']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.4.1,<4.0.0',
 'docutils>=0.19,<0.20',
 'fastapi>=0.81.0,<0.82.0',
 'textile>=4.0.2,<5.0.0',
 'uvicorn>=0.18.3,<0.19.0']

setup_kwargs = {
    'name': 'little-server',
    'version': '0.1.0',
    'description': 'A dead simple server for personal websites',
    'long_description': None,
    'author': 'megahomyak',
    'author_email': 'g.megahomyak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)

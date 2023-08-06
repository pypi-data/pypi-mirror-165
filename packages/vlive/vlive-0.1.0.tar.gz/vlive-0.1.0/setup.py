# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vlive', 'vlive.models', 'vlive.session']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.2,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'vlive',
    'version': '0.1.0',
    'description': 'Python VLIVE API',
    'long_description': '# pyvlive',
    'author': 'Kenneth V. Domingo',
    'author_email': 'hello@kvdomingo.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

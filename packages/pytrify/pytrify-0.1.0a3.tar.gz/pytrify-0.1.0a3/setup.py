# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytrify']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytrify',
    'version': '0.1.0a3',
    'description': 'A library for making Python objects immutable',
    'long_description': None,
    'author': 'Mike Salvatore',
    'author_email': 'mike.s.salvatore@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

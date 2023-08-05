# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hdruk_schema']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.0,<2.0.0',
 'prettytable>=3.3.0,<4.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'validate_email>=1.3,<2.0',
 'validators>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'hdruk-schema',
    'version': '0.1.14',
    'description': '',
    'long_description': None,
    'author': 'Ibrahim Animashaun',
    'author_email': 'iaanimashaun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['climail']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.5,<0.5.0']

setup_kwargs = {
    'name': 'climail',
    'version': '2.0.2',
    'description': 'A Command Line Interface email client written in python.',
    'long_description': 'None',
    'author': 'HRLO77',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

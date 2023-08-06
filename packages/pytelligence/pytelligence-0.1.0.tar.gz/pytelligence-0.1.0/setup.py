# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytelligence', 'pytelligence.modelling', 'pytelligence.modelling._internals']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'optuna>=2.10.1,<3.0.0',
 'pandas>=1.4.3,<2.0.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'seaborn>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'pytelligence',
    'version': '0.1.0',
    'description': 'pycaret clone aimed for simplicity and production ready code',
    'long_description': None,
    'author': 'Friedrich G. Froebel',
    'author_email': 'froebel.business@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

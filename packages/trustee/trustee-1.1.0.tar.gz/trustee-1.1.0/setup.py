# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trustee', 'trustee.enums', 'trustee.report', 'trustee.utils']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.8.1',
 'matplotlib>=3.3.1,<4.0.0',
 'numpy>=1.19.0',
 'pandas>=1.1.0,<2.0.0',
 'prettytable==3.0.0',
 'rootpath>=0.1.1,<0.2.0',
 'scikit-learn>=0.23.2',
 'scipy>=1.4.1,<2.0.0',
 'setuptools>=57.0.0,<58.0.0',
 'termcolor>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'trustee',
    'version': '1.1.0',
    'description': 'This package implements the Trustee framework to extract decision tree explanation from black-box ML models.',
    'long_description': None,
    'author': 'Arthur Selle Jacobs',
    'author_email': 'asjacobs@inf.ufrgs.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)

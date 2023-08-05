# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybuc', 'pybuc.statespace', 'pybuc.utils', 'pybuc.vectorized']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.3,<4.0.0', 'numba>=0.56.0,<0.57.0', 'pandas>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'pybuc',
    'version': '0.1.0',
    'description': 'Fast estimation of Bayesian structural time series models via Gibbs sampling.',
    'long_description': None,
    'author': 'Devin D. Garcia',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

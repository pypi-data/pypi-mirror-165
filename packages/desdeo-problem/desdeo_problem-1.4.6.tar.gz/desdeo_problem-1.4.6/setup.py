# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['desdeo_problem',
 'desdeo_problem.problem',
 'desdeo_problem.surrogatemodels',
 'desdeo_problem.testproblems',
 'desdeo_problem.testproblems.DBMOPP']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.8.0,<2.0.0',
 'descartes>=1.1.0,<2.0.0',
 'desdeo-tools>=1.7.0,<2.0.0',
 'diversipy>=0.8.0,<0.9.0',
 'optproblems>=1.2,<2.0',
 'pytest>=7.0.0,<8.0.0',
 'scikit-learn>=1.1,<2.0']

setup_kwargs = {
    'name': 'desdeo-problem',
    'version': '1.4.6',
    'description': 'This package contains the problem classes for desdeo framework.',
    'long_description': None,
    'author': 'Bhupinder Saini',
    'author_email': 'bhupinder.s.saini@jyu.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)

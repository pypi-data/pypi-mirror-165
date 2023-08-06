# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chartlyrics']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.9.1,<5.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'chartlyrics',
    'version': '0.1.0',
    'description': 'Wrapper for chartlyrics api: http://api.chartlyrics.com',
    'long_description': None,
    'author': 'matheusfillipe',
    'author_email': 'matheusfillipeag@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

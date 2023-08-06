# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sat_downloaders', 'sat_downloaders.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1']

setup_kwargs = {
    'name': 'sat-downloaders',
    'version': '0.0.4',
    'description': '',
    'long_description': 'None',
    'author': 'Martin Raspaud',
    'author_email': 'martin.raspaud@smhi.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)

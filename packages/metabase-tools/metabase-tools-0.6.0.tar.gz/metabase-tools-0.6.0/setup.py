# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metabase_tools', 'metabase_tools.models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.1,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'types-requests>=2.28.9,<3.0.0']

setup_kwargs = {
    'name': 'metabase-tools',
    'version': '0.6.0',
    'description': 'Unofficial API wrapper for Metabase plus additional helper tools',
    'long_description': None,
    'author': 'Josh Odell',
    'author_email': 'j01101111sh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

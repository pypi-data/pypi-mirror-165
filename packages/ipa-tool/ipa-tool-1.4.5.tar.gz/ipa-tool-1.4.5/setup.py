# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipa_tool']

package_data = \
{'': ['*']}

install_requires = \
['lief>=0.12.1,<0.13.0', 'rich>=12.5.1,<13.0.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['ipa-tool = ipa_tool.main:app']}

setup_kwargs = {
    'name': 'ipa-tool',
    'version': '1.4.5',
    'description': 'A simple tool for apple ipa',
    'long_description': None,
    'author': 'DrEgg',
    'author_email': 'dgg152@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.4,<4.0.0',
}


setup(**setup_kwargs)

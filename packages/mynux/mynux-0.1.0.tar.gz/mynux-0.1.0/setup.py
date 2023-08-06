# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mynux', 'mynux.cli', 'mynux.storage']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

entry_points = \
{'console_scripts': ['mynux = mynux.__main__:main'],
 'mynux.cmd': ['info = mynux.cli.info:main',
               'install = mynux.cli.install:main']}

setup_kwargs = {
    'name': 'mynux',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'axju',
    'author_email': 'moin@axju.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

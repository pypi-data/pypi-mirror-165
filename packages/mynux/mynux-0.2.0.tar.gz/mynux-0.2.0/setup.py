# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mynux', 'mynux.cli', 'mynux.storage', 'mynux.utils']

package_data = \
{'': ['*']}

install_requires = \
['tox>=3.25.1,<4.0.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

entry_points = \
{'console_scripts': ['mynux = mynux.__main__:main'],
 'mynux.cmd': ['info = mynux.cli.info:main',
               'install = mynux.cli.install:main']}

setup_kwargs = {
    'name': 'mynux',
    'version': '0.2.0',
    'description': '',
    'long_description': 'mynux - My Linux\n================\n!!!Work in progress!!!\n\nJust a dotfile manager with some extras.\n\nInstall\n-------\nIt\'s a python package, so simple install with pip::\n\n    pip install mynux\n\nor get the latest version from git::\n\n    pip install git+https://github.com/axju/mynux.git\n\nQuickstart\n----------\nIf you only want to install a single dotfile directory to your home directory,\nyou can run::\n\n    mynux install path/to/directory/or/git/url\n\nAny repo will be clone into "~/.config/mynux/repos/". After the files will\nbe linked or copy to your home directory. With the mynux.toml file you can also\ninstall package.\n\nMulti storage setup\n~~~~~~~~~~~~~~~~~~~\nAdd a repo or directory to the local config directory::\n\n    mynux add git@github.com/axju/dotfiles.git\n    mynux add /path/to/dir\n    mynux add --name my-dotfile git@github.com/axju/dotfiles.git\n\nThe command::\n\n    mynux install\n\nwill install all mynux storage from the mynux config directory. To change the order\nyou can uses the argument "--sort=name1,name2..." or change the config file\n"~./config/mynux/config.toml".\n\nDev\n---\nThis project is mange with `Poetry <https://python-poetry.org/>`_. First install\nPoetry, then run::\n\n    poetry install\n\nto install the project. Setup the per-commit hook with::\n\n    poetry run pre-commit install\n\nNow you are ready to develop. We have also a "Makefile". Look at the file to see\nthe bare commands. This ar some of them::\n\n    make install\n    make formatting\n    make test-all\n\nBugs\n----\nIf you find any bugs, pleas open an `Issue <https://github.com/axju/mynux/issues/new>`_.\n',
    'author': 'axju',
    'author_email': 'moin@axju.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

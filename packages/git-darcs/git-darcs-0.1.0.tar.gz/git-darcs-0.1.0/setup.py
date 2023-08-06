# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['git_darcs']
install_requires = \
['click>=8.1.3,<9.0.0', 'tqdm>=4.64.0,<5.0.0']

entry_points = \
{'console_scripts': ['git-darcs = git_darcs:main']}

setup_kwargs = {
    'name': 'git-darcs',
    'version': '0.1.0',
    'description': 'Incremental import of git into darcs',
    'long_description': None,
    'author': 'Jean-Louis Fuchs',
    'author_email': 'jean-louis.fuchs@adfinis.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

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
    'version': '0.1.1',
    'description': 'Incremental import of git into darcs',
    'long_description': "git-darcs - Incremental import of git into darcs\n================================================\n\nJust call `git-darcs`, it will import the history from the first commit.\nIt will remember (checkpoint) the last imported commit. If you call `git-darcs`\nagain it will import from the last checkpoint.\n\nIt will import a **linearized** version if the history, some patches might differ\nfrom the original git-commit.\n\nThe tool intentionally very minimal, it is for devs. They can read tracebacks or\nchange the code to fit better.\n\nUse a global `gitignore` to ignore `_darcs` in all your repostiories.\n\nIf you don't need any history, so you can import `git-darcs --base main^` and\nthen only track new changes from upstream.\n\nFor darcs beginners\n-------------------\n\n* You have to read the [darcs book](https://darcsbook.acmelabs.space/), you just\n  have to\n* `_darcs/pref/boring` is the equivalent of `.gitignore`, but has quite a wide\n  definition of boring by default\n\nDarcs does not handle `chmod` or symbolic-links. The easiest way to workaround\nthis, is letting `git` do the work. I have two git/darcs repositories for each\nproject.\n\n* `project` (the repository I work in) containing a `.git` and a `_darcs`\n* `project-tracking` (the repository that tracks changes from upstrream,\n   also containing a `.git` and a `_darcs`\n\nI then pull new darcs-patches from `project-tracking` into `project`. Once my\nthe changes are in upstream, I obliterate everything to the checkpoint I started\nwith and pull the patches (now via `git`) from `project-tracking`.\n\nSince I always make git-commits from the darcs-patches `git` will track `chmod`\nand symbolic-links for me.\n\nInstall\n-------\n\nIf your system python isn't 3.10 or newer use:\n\n`poetry env use $HOME/.pyenv/versions/3.10.5/bin/python3.10`\n\nto set a version installed by pyenv. You can probably set a lower version in\n`pyproject.toml`. 3.10 is just the one I am using and I know works.\n\nUsage\n-----\n\n```\nUsage: git-darcs [OPTIONS]\n\n  Incremental import of git into darcs.\n\n  By default it imports from the first commit or the last checkpoint.\n\nOptions:\n  -v, --verbose / -nv, --no-verbose\n  -w, --warn / -nw, --no-warn     Warn that repository will be cleaned\n  -b, --base TEXT                 First import from (commit-ish)\n  --help                          Show this message and exit.\n```\n",
    'author': 'Jean-Louis Fuchs',
    'author_email': 'jean-louis.fuchs@adfinis.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ganwell/git-darcs',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

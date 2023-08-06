# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git-backup']

package_data = \
{'': ['*']}

install_requires = \
['argparse', 'gitpython', 'progress', 'pylint', 'requests']

setup_kwargs = {
    'name': 'git-backup-tool',
    'version': '0.1.0',
    'description': 'Backup Github, Bitbucket or Gitlab repositories',
    'long_description': '[![Python application](https://github.com/AlexanderHieser/git-backup/actions/workflows/pylint.yml/badge.svg)](https://github.com/AlexanderHieser/git-backup/actions/workflows/pylint.yml)\n\n# Git Backup\n\n![Welcome](/docu/git_backup_header.png)\nSmall CLI which helps to clone all user repositories on github.com, gitlab.com, bitbucket.com.\n\n## Usage\n\nProvide the following parameters to the cmd:\n\n```bash\n-h, --help    Show this help message and exit\n-t ACCESS_TOKEN  Your Github API Access Token\n-p DESTINATION   Backup destination path\n--mirror         Mirror repositories\n-u USERNAME      Username filtering\n```\n\n## Contribution\nJust create a PR, no guidlines at the moment ;)\n',
    'author': 'Alexander Hieser',
    'author_email': 'Alexander.Hieser@online.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

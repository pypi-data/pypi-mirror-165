# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['github_repo_traffic']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.55,<2.0',
 'asciichartpy>=1.5.25,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['repo-data = github_repo_traffic.data:main',
                     'repo-readme = github_repo_traffic.readme:main']}

setup_kwargs = {
    'name': 'github-repo-traffic',
    'version': '2.0.0',
    'description': '',
    'long_description': None,
    'author': 'Will Humphlett',
    'author_email': 'will@humphlett.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

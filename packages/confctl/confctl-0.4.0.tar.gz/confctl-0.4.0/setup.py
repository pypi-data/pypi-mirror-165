# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['confctl']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.11.1,<4']

entry_points = \
{'console_scripts': ['confctl = confctl.cli:main']}

setup_kwargs = {
    'name': 'confctl',
    'version': '0.4.0',
    'description': 'Simple configuration management',
    'long_description': '<p align="center">\n    <a href="https://pypi.org/project/confctl/">\n        <img src="https://badge.fury.io/py/confctl.svg" alt="Package version">\n    </a>\n</p>\n\n# confctl\n\nBuild-system-like approach to manage your configs.\n\n```sh\n$ confctl //tools/kitty\n```\n\nTBD\n',
    'author': 'miphreal',
    'author_email': 'miphreal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/miphreal/confctl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

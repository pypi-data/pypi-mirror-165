# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arguebuf_cli']

package_data = \
{'': ['*']}

install_requires = \
['arguebuf>=1.0.3,<2.0.0',
 'deepl-pro>=0.1.4,<0.2.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['arguebuf = arguebuf_cli.app:cli']}

setup_kwargs = {
    'name': 'arguebuf-cli',
    'version': '1.1.3',
    'description': 'Command line interface for interacting with argument graphs.',
    'long_description': '# Arguebuf CLI\n\nThis project aims at providing some tools to simplify dealing with structured argument graphs.\nAmong others, it is possible to convert graphs between different formats, translate them, and render images using graphviz.\nThe library can easily be installed using pip:\n\n`pip install arguebuf-cli`\n\nAfterwards, you can execute it by calling `arguebuf`, for example:\n\n`arguebuf --help`\n',
    'author': 'Mirko Lenz',
    'author_email': 'info@mirko-lenz.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://recap.uni-trier.de',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beam', 'beam.clients', 'beam.clients.syncthing', 'beam.commands']

package_data = \
{'': ['*']}

install_requires = \
['python-syncthing-client>=0.1.1,<0.2.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'typer>=0.6.1,<0.7.0',
 'websockets>=10.3,<11.0',
 'yamldataclassconfig>=1.5.0,<2.0.0']

entry_points = \
{'console_scripts': ['beam = beam.cli:app']}

setup_kwargs = {
    'name': 'beam-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Luke Lombardi',
    'author_email': 'luke@slai.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)

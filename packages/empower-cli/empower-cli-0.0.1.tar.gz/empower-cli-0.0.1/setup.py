# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli',
 'cli.commands',
 'cli.commands.auth',
 'cli.commands.empower_api',
 'cli.commands.empower_discovery',
 'cli.common',
 'cli.common.auth']

package_data = \
{'': ['*'], 'cli.common.auth': ['templates/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'pickleDB>=0.9.2,<0.10.0',
 'pydantic>=1.9.1,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'python-keycloak>=2.0.0,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'typer>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['empowercli = cli.main:app']}

setup_kwargs = {
    'name': 'empower-cli',
    'version': '0.0.1',
    'description': 'PLACEHOLDER',
    'long_description': 'PLACEHOLDER',
    'author': 'Brian Aiken',
    'author_email': 'baiken@hitachisolutions.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hitachisolutionsamerica/empower/tree/development/tools/empower_cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

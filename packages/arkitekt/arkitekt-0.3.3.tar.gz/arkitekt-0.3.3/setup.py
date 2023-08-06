# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arkitekt',
 'arkitekt.apps',
 'arkitekt.cli',
 'arkitekt.cli.dev',
 'arkitekt.cli.prod',
 'arkitekt.qt',
 'arkitekt.test']

package_data = \
{'': ['*']}

install_requires = \
['fakts>=0.2.6,<0.3.0',
 'herre>=0.2.6,<0.3.0',
 'mikro>=0.2.8,<0.3.0',
 'rekuest>=0.0.8,<0.0.9',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['arkitekt = arkitekt.cli.main:entrypoint']}

setup_kwargs = {
    'name': 'arkitekt',
    'version': '0.3.3',
    'description': 'rpc and node backbone',
    'long_description': None,
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

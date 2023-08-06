# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['appstrap']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['appstrap = appstrap.core:main']}

setup_kwargs = {
    'name': 'appstrap',
    'version': '0.1.0',
    'description': 'A modern configuration interface for Python applications.',
    'long_description': '# appstrap\n\nAppStrap provides a configuration interface for Python applications\n\n## Objectives and Stretch Goals*\n\n- ...',
    'author': 'Mark Beacom',
    'author_email': 'm@beacom.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://mbeacom.github.io/appstrap/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

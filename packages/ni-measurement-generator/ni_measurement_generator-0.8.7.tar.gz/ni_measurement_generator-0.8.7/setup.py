# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ni_measurement_generator']

package_data = \
{'': ['*'], 'ni_measurement_generator': ['templates/*']}

install_requires = \
['Mako>=1.2.1,<2.0.0', 'click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['ni-measurement-generator = '
                     'ni_measurement_generator.template:create_measurement']}

setup_kwargs = {
    'name': 'ni-measurement-generator',
    'version': '0.8.7',
    'description': 'A utility for generating Python measurement service projects that use the ni_measurement_service',
    'long_description': None,
    'author': 'NI',
    'author_email': 'opensource@ni.com',
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

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idasen_controller']

package_data = \
{'': ['*'], 'idasen_controller': ['example/*']}

install_requires = \
['PyYAML>=5.4.1,<=6.0.0',
 'aiohttp==3.8.1',
 'appdirs==1.4.4',
 'bleak>=0.14.2,<=0.16.0']

entry_points = \
{'console_scripts': ['idasen-controller = idasen_controller.main:init']}

setup_kwargs = {
    'name': 'idasen-controller',
    'version': '2.0.2rc2',
    'description': 'Command line tool for controlling the Ikea Idasen (Linak) standing desk',
    'long_description': None,
    'author': 'Rhys Tyers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.3',
}


setup(**setup_kwargs)

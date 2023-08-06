# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airthings_ble']

package_data = \
{'': ['*']}

install_requires = \
['bleak-retry-connector>=1.8.0,<2.0.0', 'bleak>=0.15.1,<0.16.0']

extras_require = \
{'docs': ['Sphinx>=5.0,<6.0',
          'sphinx-rtd-theme>=1.0,<2.0',
          'myst-parser>=0.18,<0.19']}

setup_kwargs = {
    'name': 'airthings-ble',
    'version': '0.5.0',
    'description': 'Manage Airthings BLE devices',
    'long_description': '# airthings-ble\n\nLibrary to control Airthings devices through BLE, primarily meant to be used in Home Assistant.\n',
    'author': 'J. Nick Koston',
    'author_email': 'nick@koston.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vincegio/airthings-ble',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

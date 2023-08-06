# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_redcap', 'tap_redcap.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.4.4,<0.5.0']

entry_points = \
{'console_scripts': ['tap-redcap = tap_redcap.tap:TapRedCap.cli']}

setup_kwargs = {
    'name': 'tap-redcap',
    'version': '0.0.1',
    'description': '`tap-redcap` is a Singer tap for redcap, built with the Meltano SDK for Singer Taps.',
    'long_description': None,
    'author': 'Nick Van Kuren',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)

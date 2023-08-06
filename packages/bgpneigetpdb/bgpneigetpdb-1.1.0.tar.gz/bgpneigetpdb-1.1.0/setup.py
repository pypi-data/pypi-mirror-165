# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bgpneigetpdb']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'napalm>=4.0.0,<5.0.0']

entry_points = \
{'console_scripts': ['bgpneigetpdb = bgpneigetpdb.cli:cli']}

setup_kwargs = {
    'name': 'bgpneigetpdb',
    'version': '1.1.0',
    'description': 'Get BGP Neighbours from network devices for PDB',
    'long_description': '# bgpneigetbdp\nGet BGP neighbours from network devices for use in a peering database\n',
    'author': 'Rob Woodward',
    'author_email': 'rob@emailplus.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/robwdwd/bgpneigetpdb',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

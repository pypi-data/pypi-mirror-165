# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypatches',
 'pypatches.code',
 'pypatches.transform',
 'pypatches.util',
 'pypatches.util.libs']

package_data = \
{'': ['*']}

install_requires = \
['angr>=9.2.7,<10.0.0',
 'archinfo>=9.2.7,<10.0.0',
 'cle>=9.2.7,<10.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'keystone-engine>=0.9.2,<0.10.0',
 'lief>=0.12.1,<0.13.0',
 'pysquishy>=0.1.17,<0.2.0',
 'rich>=12.4.4,<13.0.0']

setup_kwargs = {
    'name': 'pypatches',
    'version': '0.1.4',
    'description': 'Binary patching framework',
    'long_description': '# PyPatches\n\n[![Documentation Status](https://readthedocs.org/projects/binary-patches/badge/?version=main)](https://binary-patches.readthedocs.io/en/main/?badge=main)\n\n## Documentation\n\nDocumentation can be found [here](https://binary-patches.readthedocs.io).\n\n## Installation\n\nUp-to-date installation instructions can be found [here](docs/install.md).\n\n',
    'author': 'novafacing',
    'author_email': 'rowanbhart@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pbsrollout']

package_data = \
{'': ['*']}

install_requires = \
['kubernetes>=24.2.0,<25.0.0',
 'pync>=2.0.3,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'shellpy>=0.5.1,<0.6.0',
 'simple-term-menu>=1.5.0,<2.0.0']

entry_points = \
{'console_scripts': ['pbsrollout = pbsrollout.main:main']}

setup_kwargs = {
    'name': 'pbsrollout',
    'version': '0.2.6',
    'description': '',
    'long_description': None,
    'author': 'dimitri',
    'author_email': 'dimitriwyzlic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['watchmen_indicator_surface',
 'watchmen_indicator_surface.data',
 'watchmen_indicator_surface.meta',
 'watchmen_indicator_surface.util']

package_data = \
{'': ['*']}

install_requires = \
['watchmen-indicator-kernel==16.2.5', 'watchmen-rest==16.2.5']

extras_require = \
{'mongodb': ['watchmen-storage-mongodb==16.2.5'],
 'mssql': ['watchmen-storage-mssql==16.2.5'],
 'mysql': ['watchmen-storage-mysql==16.2.5'],
 'oracle': ['watchmen-storage-oracle==16.2.5'],
 'postgresql': ['watchmen-storage-postgresql==16.2.5']}

setup_kwargs = {
    'name': 'watchmen-indicator-surface',
    'version': '16.2.5',
    'description': '',
    'long_description': 'None',
    'author': 'botlikes',
    'author_email': '75356972+botlikes456@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

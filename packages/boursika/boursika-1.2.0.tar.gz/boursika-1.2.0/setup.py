# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boursika', 'boursika.utils']

package_data = \
{'': ['*']}

install_requires = \
['jdatetime>=3,<4',
 'pandas>=1,<2',
 'python-dateutil>=2,<3',
 'requests>=2,<3',
 'websocket-client>=1,<2']

setup_kwargs = {
    'name': 'boursika',
    'version': '1.2.0',
    'description': 'client for boursika-engine platform',
    'long_description': None,
    'author': 'Mahdi Sadeghi',
    'author_email': 'mail2mahsad@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://docs.boursika-engine.ir',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

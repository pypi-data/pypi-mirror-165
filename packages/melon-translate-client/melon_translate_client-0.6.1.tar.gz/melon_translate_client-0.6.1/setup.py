# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['melon_translate_client', 'melon_translate_client.tests']

package_data = \
{'': ['*']}

install_requires = \
['python-decouple>=3.6,<4.0', 'redis>=4.3.0,<5.0.0', 'requests>=2.27.0']

setup_kwargs = {
    'name': 'melon-translate-client',
    'version': '0.6.1',
    'description': 'Client package for melon-translate.',
    'long_description': None,
    'author': 'sam',
    'author_email': 'contact@justsam.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

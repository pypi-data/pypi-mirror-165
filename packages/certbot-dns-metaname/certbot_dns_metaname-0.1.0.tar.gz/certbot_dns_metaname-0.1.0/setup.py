# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['certbot_dns_metaname']

package_data = \
{'': ['*']}

install_requires = \
['certbot>=1.29.0,<2.0.0', 'mock>=4.0.3,<5.0.0', 'requests-mock>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'certbot-dns-metaname',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Taylor Kettle',
    'author_email': 'tin.teapot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

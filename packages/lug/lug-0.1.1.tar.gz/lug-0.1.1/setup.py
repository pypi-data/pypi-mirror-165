# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lug']

package_data = \
{'': ['*']}

install_requires = \
['toolchest-client>=0.9.31,<0.10.0']

setup_kwargs = {
    'name': 'lug',
    'version': '0.1.1',
    'description': 'lug',
    'long_description': '# Lug',
    'author': 'Bryce Cai',
    'author_email': 'bryce@trytoolchest.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trytoolchest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

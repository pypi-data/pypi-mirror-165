# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pystreasy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pystreasy',
    'version': '0.1.2',
    'description': 'makes working with strings easy',
    'long_description': None,
    'author': 'ablesoftwaredev',
    'author_email': '48694187+ablesoftwaredev@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ablesoftwaredev/pystreasy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

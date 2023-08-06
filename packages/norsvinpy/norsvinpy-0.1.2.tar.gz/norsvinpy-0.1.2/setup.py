# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['norsvinpy']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'norsvinpy',
    'version': '0.1.2',
    'description': 'Demo environement for ML development',
    'long_description': '# Norsvinpy\n\nRepository of useful functions in use in Norsvin',
    'author': 'Christopher',
    'author_email': 'christopher.coello@norsvin.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

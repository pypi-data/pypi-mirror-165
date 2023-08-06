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
    'version': '0.1.1',
    'description': 'Demo environement for ML development',
    'long_description': "# Development environment for ML projects\n\n## Local environment \n\nHere are the steps to start developing and run code *locally*\n * Clone this repo\n * If you don't have python installed on your machine, install Python\n * If you don't have poetry installed on your Python environement, type\n    ```bash\n    pip install poetry\n    ```\n * Install the necessary dependencies in a virtual environment\n    ```bash\n    poetry install\n    ```\n * Run the command in the virtual env\n    ```bash\n    poetry run python -m app\n    ```\n * Add dependencies to the project, for example the library requests in this case\n    ```bash\n    poetry add requests\n    ```\n## Docker environment \nHere are the steps to start developing and run code *on a Docker image*\n * If you don't have Docker installed on your machine, install Docker\n * Build an image based on the Dockerfile of this repo\n    ```bash\n    docker build -t ml-env .\n    ```\n * Run the image\n    ```bash \n    docker run -it ml-env\n    ```\n\n## Testing \nThe tests are included in the tests folder, and uses pytest as testing library.",
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

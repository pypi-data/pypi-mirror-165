# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['environ_loader']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1']

entry_points = \
{'console_scripts': ['environ-loader = environ_loader.__main__:main']}

setup_kwargs = {
    'name': 'environ-loader',
    'version': '0.0.1',
    'description': 'Environ Loader',
    'long_description': "# Environ Loader\n\nA module for loading environment variables from various sources, like Windows .bat files and Bash .sh files.\n\nSometimes when writing a Python script, you want to load environment variables are defined in a text file. For example, when running Conan with the virtualenv generator,\nConan will generate shell files for Windows and Linux that contain variables like PATH that are configured to use the library/tool. So, if you are installing\na tool that the script uses with Conan, then you will have to load the environment variables before calling the tool. This is actually the original motivation\nfor the module.\n\nIt is not very sophisticated yet, only simple variable declarations are supported right now (for examples, Bash's $VAR style variable expansion is not supported, only ${VAR}).\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Environ Loader_ via [pip] from [PyPI]:\n\n```console\n$ pip install environ-loader\n```\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Environ Loader_ is free and open source software.\n\n",
    'author': 'CD Clark III',
    'author_email': 'clifton.clark@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CD3/environ-loader',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

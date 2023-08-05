# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jarvis_tasks_library']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0', 'types-python-dateutil>=2.8.19,<3.0.0']

setup_kwargs = {
    'name': 'jarvis-tasks-library',
    'version': '1.17.0',
    'description': '',
    'long_description': None,
    'author': 'Juan Rodriguez',
    'author_email': 'angel.neb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

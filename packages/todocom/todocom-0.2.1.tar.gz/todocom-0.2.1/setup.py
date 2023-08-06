# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['todocom']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['todo = todocom.cli:main']}

setup_kwargs = {
    'name': 'todocom',
    'version': '0.2.1',
    'description': '',
    'long_description': 'None',
    'author': 'avivfaraj',
    'author_email': 'avivfaraj4@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

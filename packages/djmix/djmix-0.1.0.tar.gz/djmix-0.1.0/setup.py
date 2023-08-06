# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['djmix', 'djmix.models']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'djmix',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Taejun Kim',
    'author_email': 'taejun@kaist.ac.kr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djmix', 'djmix.models']

package_data = \
{'': ['*']}

install_requires = \
['cvxpy>=1.2.1,<2.0.0',
 'joblib>=1.1.0,<2.0.0',
 'librosa>=0.9.2,<0.10.0',
 'madmom>=0.16.1,<0.17.0',
 'pandas>=1.4.3,<2.0.0',
 'pydantic>=1.9.2,<2.0.0',
 'pydub>=0.25.1,<0.26.0',
 'pytsmod>=0.3.5,<0.4.0',
 'scikit-image>=0.19.3,<0.20.0',
 'yt-dlp']

setup_kwargs = {
    'name': 'djmix',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Taejun Kim',
    'author_email': 'taejun@kaist.ac.kr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)

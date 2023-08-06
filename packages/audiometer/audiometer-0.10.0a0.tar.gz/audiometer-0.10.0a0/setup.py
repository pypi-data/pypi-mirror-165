# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.audiometer']

package_data = \
{'': ['*']}

install_requires = \
['pydub>=0.25.1,<0.26.0']

setup_kwargs = {
    'name': 'audiometer',
    'version': '0.10.0a0',
    'description': 'Calculate audio level meter.',
    'long_description': None,
    'author': 'novdov',
    'author_email': 'sunwoong@pozalabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)

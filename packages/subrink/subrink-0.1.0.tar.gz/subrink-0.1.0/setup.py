# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['subrink']
setup_kwargs = {
    'name': 'subrink',
    'version': '0.1.0',
    'description': 'Sum of two digits',
    'long_description': None,
    'author': 'Brinkinvision',
    'author_email': 'brinkinvision@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['batch']
setup_kwargs = {
    'name': 'batchable',
    'version': '0.2.1',
    'description': 'Hide your batch logic away from the actual code.',
    'long_description': None,
    'author': 'L3viathan',
    'author_email': 'git@l3vi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

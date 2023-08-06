# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aviat']
entry_points = \
{'console_scripts': ['aviat = aviat:main']}

setup_kwargs = {
    'name': 'aviat',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'RedMooner',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

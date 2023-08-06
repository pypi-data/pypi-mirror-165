# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['speiseplan']
entry_points = \
{'console_scripts': ['speiseplan = speiseplan:main']}

setup_kwargs = {
    'name': 'speiseplan',
    'version': '0.3.1',
    'description': '',
    'long_description': None,
    'author': 'Markus Quade',
    'author_email': 'info@markusqua.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

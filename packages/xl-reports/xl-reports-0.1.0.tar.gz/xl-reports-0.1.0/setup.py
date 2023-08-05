# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['xl_reports']
install_requires = \
['mypy>=0.971,<0.972', 'openpyxl>=3.0.10,<4.0.0']

setup_kwargs = {
    'name': 'xl-reports',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Dustin Sampson',
    'author_email': 'dustin@sparkgeo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

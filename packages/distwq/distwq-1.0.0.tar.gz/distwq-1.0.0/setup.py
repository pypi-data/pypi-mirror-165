# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['distwq']
install_requires = \
['black>=22.6.0,<23.0.0',
 'flake8>=5.0.4,<6.0.0',
 'isort>=5.10.1,<6.0.0',
 'mpi4py>=3.1.3,<4.0.0',
 'numpy>=1.23.1,<2.0.0',
 'pylint>=2.15.0,<3.0.0',
 'pytest>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'distwq',
    'version': '1.0.0',
    'description': 'Distributed queue operations with mpi4py',
    'long_description': None,
    'author': 'Ivan Raikov',
    'author_email': 'ivan.g.raikov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

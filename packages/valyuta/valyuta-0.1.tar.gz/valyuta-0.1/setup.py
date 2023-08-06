# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['valyuta']
install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'valyuta',
    'version': '0.1',
    'description': '',
    'long_description': '```python\nfrom valyuta import convert, info\nvalyuta("USD","UZS",100)\ninfo("RUB")\n```\n',
    'author': 'coderstack404',
    'author_email': 'coderstack404@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

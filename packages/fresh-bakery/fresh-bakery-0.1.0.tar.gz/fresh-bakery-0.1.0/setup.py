# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bakery']

package_data = \
{'': ['*']}

modules = \
['py']
entry_points = \
{'pytest11': ['bakery_mock = bakery.testbakery']}

setup_kwargs = {
    'name': 'fresh-bakery',
    'version': '0.1.0',
    'description': 'Bake your dependencies stupidly simple!',
    'long_description': '',
    'author': 'Dmitry Makarov',
    'author_email': 'mit.makaroff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.11',
}


setup(**setup_kwargs)

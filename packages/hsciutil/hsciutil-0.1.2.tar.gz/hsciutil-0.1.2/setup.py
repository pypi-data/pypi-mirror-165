# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hsciutil', 'hsciutil.fs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hsciutil',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Eetu Mäkelä',
    'author_email': 'eetu.makela@helsinki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

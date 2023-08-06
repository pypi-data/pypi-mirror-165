# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utils_joecatin']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'utils-joecatin',
    'version': '0.0.1',
    'description': 'personal utility package for Python3',
    'long_description': '# utils-py\n\nPersonal utility package for Python3\n\n![Tests](https://github.com/joecatin/utils-py/actions/workflows/tests.yml/badge.svg)\n',
    'author': 'joe',
    'author_email': 'catinjoe@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/joecatin/utils-py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

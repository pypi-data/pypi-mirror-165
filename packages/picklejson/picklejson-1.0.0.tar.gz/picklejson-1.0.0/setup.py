# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['picklejson']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=21.3,<22.0']

setup_kwargs = {
    'name': 'picklejson',
    'version': '1.0.0',
    'description': 'Library that allows you to serialize any python object into JSON',
    'long_description': None,
    'author': 'Dogeek',
    'author_email': 'simon.bordeyne@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['patmlkit', 'patmlkit.coco', 'patmlkit.image', 'patmlkit.json']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'patmlkit',
    'version': '0.1.1',
    'description': 'Pain and tears ML kit - library created to support my journey via PHD',
    'long_description': None,
    'author': 'Michal Karol',
    'author_email': 'michal.p.karol@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

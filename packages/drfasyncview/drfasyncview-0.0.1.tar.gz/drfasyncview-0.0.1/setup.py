# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drfasyncview']

package_data = \
{'': ['*']}

install_requires = \
['django>=4.1.0,<5.0.0', 'djangorestframework<=3.13.1']

setup_kwargs = {
    'name': 'drfasyncview',
    'version': '0.0.1',
    'description': 'AsyncAPIView allows you to use async handlers keeping the compatibility with django-rest-framework',
    'long_description': '# drf-async-view\nAsyncAPIView allows you to use async handlers keeping the compatibility with django-rest-framework\n',
    'author': 'hisdream86',
    'author_email': 'hisdream86@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hisdream86/drf-async-view',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

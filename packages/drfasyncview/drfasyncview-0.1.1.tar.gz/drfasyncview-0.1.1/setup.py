# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drfasyncview']

package_data = \
{'': ['*']}

install_requires = \
['django<=4.1.0', 'djangorestframework<=3.13.1']

setup_kwargs = {
    'name': 'drfasyncview',
    'version': '0.1.1',
    'description': 'AsyncAPIView allows you to use async handlers keeping the compatibility with django-rest-framework',
    'long_description': '# drf-async-view\n\nDjango supports [AsyncView](https://docs.djangoproject.com/en/4.1/releases/4.1/#asynchronous-handlers-for-class-based-views) from 4.1 to support writing asynchronous handlers.\n\n`AsyncAPIView` allows you to use async handlers keeping the compatibility with django-rest-framework as well.\n\n## Installation\n\nYou can install the latest release from pypi:\n\n```sh\n$ pip install drfasyncview\n```\n\n## How to use\n\n### Example\n\n```python\nimport asyncio\n\nfrom django.contrib.auth.models import User\nfrom django.db import models\nfrom django.http import HttpRequest, JsonResponse\nfrom rest_framework.authentication import BaseAuthentication\nfrom rest_framework.permissions import BasePermission\nfrom rest_framework.throttling import BaseThrottle\nfrom typing import Optional, Tuple\n\nfrom drfasyncview import AsyncRequest, AsyncAPIView\n\n\nclass AsyncAuthentication(BaseAuthentication):    \n    async def authenticate(self, request: AsyncRequest) -> Optional[Tuple[User, str]]:\n        await asyncio.sleep(0.01)\n        return None\n\n\nclass AsyncPermission(BasePermission):\n    async def has_permission(self, request: AsyncRequest, view: AsyncAPIView) -> bool:\n        await asyncio.sleep(0.01)\n        return True\n\n\nclass AsyncThrottle(BaseThrottle):\n    async def allow_request(self, request: AsyncRequest, view: AsyncAPIView) -> bool:\n        await asyncio.sleep(0.01)\n        return True\n\n\nclass Product(models.Model):\n    name = models.CharField(max_length=256, unique=True)\n    price = models.IntegerField()\n\n\nclass ProductsView(AsyncAPIView):\n    authentication_classes = [AsyncAuthentication]\n    permission_classes = [AsyncPermission]\n    throttle_classes = [AsyncThrottle]\n\n    async def post(self, request: HttpRequest) -> JsonResponse:\n        name = request.data["name"]\n        price = request.data["price"]\n\n        product = await Product.objects.acreate(name=name, price=price)\n\n        return JsonResponse(\n            data={"name": product.name, "price": product.price},\n            status=200,\n        )\n```\n',
    'author': 'hisdream86',
    'author_email': 'hisdream86@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hisdream86/drf-async-view',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '<=3.8',
}


setup(**setup_kwargs)

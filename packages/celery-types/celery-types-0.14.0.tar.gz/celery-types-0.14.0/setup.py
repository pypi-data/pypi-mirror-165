# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amqp-stubs',
 'billiard-stubs',
 'celery-stubs',
 'django_celery_results-stubs',
 'ephem-stubs',
 'kombu-stubs',
 'vine-stubs']

package_data = \
{'': ['*'],
 'celery-stubs': ['app/*',
                  'apps/*',
                  'backends/*',
                  'concurrency/*',
                  'loaders/*',
                  'utils/*',
                  'utils/dispatch/*',
                  'worker/*'],
 'kombu-stubs': ['transport/*', 'utils/*']}

install_requires = \
['typing-extensions>=3.10.0,<5.0.0']

setup_kwargs = {
    'name': 'celery-types',
    'version': '0.14.0',
    'description': 'Type stubs for Celery and its related packages',
    'long_description': "# celery-types [![PyPI](https://img.shields.io/pypi/v/celery-types.svg)](https://pypi.org/project/celery-types/)\n\nType stubs for celery related projects:\n\n- [`celery`](https://github.com/celery/celery)\n- [`django-celery-results`](https://github.com/celery/django-celery-results)\n- [`amqp`](http://github.com/celery/py-amqp)\n- [`kombu`](https://github.com/celery/kombu)\n- [`billiard`](https://github.com/celery/billiard)\n- [`vine`](https://github.com/celery/vine)\n- [`ephem`](https://github.com/brandon-rhodes/pyephem)\n\n## install\n\n```shell\npip install celery-types\n```\n\nYou'll also need to monkey patch `Task` so generic params can be provided:\n\n```python\nfrom celery.app.task import Task\nTask.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)\n```\n\n## dev\n\n```shell\npoetry install\n\n# run formatting, linting, and typechecking\ns/lint\n\n# build and publish\npoetry publish --build\n```\n\n## related\n\n- <https://github.com/sbdchd/django-types>\n- <https://github.com/sbdchd/djangorestframework-types>\n- <https://github.com/sbdchd/mongo-types>\n- <https://github.com/sbdchd/msgpack-types>\n",
    'author': 'Steve Dignam',
    'author_email': 'steve@dignam.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sbdchd/celery-types',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

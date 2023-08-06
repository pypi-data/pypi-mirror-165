# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['translate',
 'translate.core',
 'translate.core.utils',
 'translate.service',
 'translate.service.management',
 'translate.service.management.commands',
 'translate.service.migrations',
 'translate.service.tests']

package_data = \
{'': ['*'],
 'translate.service': ['static/assets/*',
                       'static/assets/img/*',
                       'static/css/*',
                       'static/js/*',
                       'templates/*'],
 'translate.service.tests': ['fixtures/*', 'fixtures/locale/de/LC_MESSAGES/*']}

install_requires = \
['Django>=4.0.7,<5.0.0',
 'django-admin-inline-paginator>=0.3.0,<0.4.0',
 'django-auditlog>=1.0.0,<2.0.0',
 'django-baton>=2.3.0,<3.0.0',
 'django-health-check>=3.16.5,<4.0.0',
 'django-model-utils>=4.2.0,<5.0.0',
 'djangorestframework>=3.13.1,<4.0.0',
 'drf-spectacular>=0.22.0,<0.23.0',
 'polib>=1.1.1,<2.0.0',
 'psycopg2-binary==2.9.1',
 'python-decouple>=3.5,<4.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'redis>=4.3.4,<5.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'melon-translate',
    'version': '0.6.1',
    'description': 'Melon-translate is a micro service for easing localisation and translation.',
    'long_description': None,
    'author': 'sam',
    'author_email': 'contact@justsam.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

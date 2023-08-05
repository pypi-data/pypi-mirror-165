# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_route',
 'django_route.conf',
 'django_route.migrations',
 'django_route.signals']

package_data = \
{'': ['*']}

install_requires = \
['Django']

setup_kwargs = {
    'name': 'django-route',
    'version': '0.3.0',
    'description': 'Conditional url routing for django',
    'long_description': "django-route\n============\n\nConditional url routing for django\n\n.. image:: https://travis-ci.org/vinayinvicible/django-route.svg\n    :target: https://travis-ci.org/vinayinvicible/django-route\n\n.. image:: https://codecov.io/gh/vinayinvicible/django-route/coverage.svg?branch=master\n    :target: https://codecov.io/gh/vinayinvicible/django-route\n\nInstallation\n------------\n\npip install django-route\n\nContributing\n------------\n\n1. Fork it!\n2. Create your feature branch: `git checkout -b my-new-feature`\n3. Commit your changes: `git commit -am 'Add some feature'`\n4. Push to the branch: `git push origin my-new-feature`\n5. Submit a pull request :D\n\nUsage\n-----\n\n1. Create a router for the url\n2. Add destination url\n3. Provide the action (301/302/proxy)\n4. Describe the condition in templating language\n\nLicense\n-------\n\nThis project is licensed under the MIT License - see the LICENSE_ file for details\n\n.. _LICENSE: https://github.com/vinayinvicible/django-route/blob/master/LICENSE\n",
    'author': 'Vinay Karanam',
    'author_email': 'vinayinvicible@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vinayinvicible/django-route',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

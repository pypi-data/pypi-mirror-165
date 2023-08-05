# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sssoon', 'sssoon.migrations']

package_data = \
{'': ['*'],
 'sssoon': ['static/sssoon/css/*',
            'static/sssoon/css/fonts/*',
            'static/sssoon/fonts/*',
            'static/sssoon/img/*',
            'static/sssoon/img/sprites/*',
            'static/sssoon/js/*',
            'static/sssoon/js/framework/*',
            'static/sssoon/js/language/*',
            'templates/sssoon/*']}

install_requires = \
['Django', 'django-recaptcha>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'django-sssoon',
    'version': '0.1.9',
    'description': 'A simple Django app to add a beautiful coming soon page to your project.',
    'long_description': None,
    'author': 'Hareem Adderley',
    'author_email': 'HADDERLEY@KINGPINAPPS.COM',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

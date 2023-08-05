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
    'version': '0.1.11',
    'description': 'A simple Django app to add a beautiful coming soon page to your project.',
    'long_description': '\ndjango-sssoon\n=============\n\nDjango-sssoon is a simple Django app to add beautiful coming soon webpage to your django website. This template is\nbased on on Bootstrap 3 and designed by [Creative Tim](https://www.creative-tim.com/).\n\n![Screenshot](./docs/images/screencapture.png "Screenshot")\n\nDetailed documentation is in the "docs" directory.\n\nQuick start\n-----------\n1. django-sssoon is available on the Python Package Index (PyPI), so it can be installed with standard Python tools like `pip` or `easy_install`:\n\n```python\npip install django-sssoon\n```\n\n2. Add "sssoon" to your INSTALLED_APPS setting like this:\n\n```python\nINSTALLED_APPS = [\n    ...\n    \'sssoon\',\n]\n```\n\n2. Include the sssoon URLconf in your project urls.py like this to make your index page coming sssoon:\n\n```python\nurl(r\'^\', include(\'sssoon.urls\', namespace="sssoon")),\n```\n\n3. Collect static files\n\n```python\npython manage.py collectstatic\n```\n\n4. Start the development server and visit http://127.0.0.1:8000/\n',
    'author': 'Hareem Adderley',
    'author_email': 'HADDERLEY@KINGPINAPPS.COM',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kingpin-Apps/django-sssoon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

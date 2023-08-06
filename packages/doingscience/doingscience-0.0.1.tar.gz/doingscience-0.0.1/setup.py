# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doingscience']

package_data = \
{'': ['*']}

install_requires = \
['backoff==2.0.1',
 'beautifulsoup4==4.11.1',
 'pandas==1.4.2',
 'pyfarmhash==0.2.2',
 'requests==2.27.1',
 'simplejson==3.17.2']

setup_kwargs = {
    'name': 'doingscience',
    'version': '0.0.1',
    'description': 'This package includes multipurpose fuctions to simplify your life.',
    'long_description': '# DoingScience',
    'author': 'Iasonas Tragakis',
    'author_email': 'iasonas@doing-science.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)

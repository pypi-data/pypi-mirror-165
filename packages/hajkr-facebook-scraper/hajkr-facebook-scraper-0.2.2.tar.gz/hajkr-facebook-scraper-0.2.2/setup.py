# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hajkr_facebook_scraper']

package_data = \
{'': ['*']}

install_requires = \
['facebook-scraper>=0.2,<0.3']

entry_points = \
{'console_scripts': ['hajkr-facebook-scraper = '
                     'hajkr_facebook_scraper.__main__:run']}

setup_kwargs = {
    'name': 'hajkr-facebook-scraper',
    'version': '0.2.2',
    'description': '',
    'long_description': None,
    'author': 'Tadej Hribar',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

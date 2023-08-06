# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easy_post_twitter']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'tweepy>=4.10.0,<5.0.0']

setup_kwargs = {
    'name': 'easy-post-twitter',
    'version': '1.0.3',
    'description': 'The easy way to send posts to twitter.',
    'long_description': None,
    'author': 'Thiago Oliveira',
    'author_email': 'thiceconelo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

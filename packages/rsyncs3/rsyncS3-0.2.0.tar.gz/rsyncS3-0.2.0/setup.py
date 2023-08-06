# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rsyncs3']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.64,<2.0.0']

setup_kwargs = {
    'name': 'rsyncs3',
    'version': '0.2.0',
    'description': 'Utility to easily download objects from Amazon S3 buckets.',
    'long_description': None,
    'author': 'Dephy Inc.',
    'author_email': 'software@dephy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DephyInc/rsyncS3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

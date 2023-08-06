# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logger_hub_drh']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'logger-hub-drh',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'daniel-rodriguez-hernandez',
    'author_email': 'daniel.rodriguez.hernandez@pwc.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

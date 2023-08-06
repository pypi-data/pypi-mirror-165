# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solmate_sdk']

package_data = \
{'': ['*']}

install_requires = \
['websockets>=10.3,<11.0']

setup_kwargs = {
    'name': 'solmate-sdk',
    'version': '0.1.0',
    'description': 'Software Development Kit for the EET SolMate',
    'long_description': '# solmate-sdk\n\nAll you need to integrate SolMate into your home automation system and more (coming soon)\n',
    'author': 'EET',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

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
    'version': '0.1.4',
    'description': 'Software Development Kit for the EET SolMate',
    'long_description': '# EET SolMate SDK\n\nAll you need to integrate your [EET SolMate](https://www.eet.energy) into your home automation system - or really any Python-based system!\nKeep in mind that this is **work in progress**.\n\nThis Python SDK provides a class-based API Client which lets you:\n\n1. Login to your SolMate with serial number and password which returns an authentication token.\n2. Connect to your SolMate with the authentication token.\n3. Get live values of your SolMate.\n4. Check if your SolMate is online.\n\nFor any inquiries about, or problems with, the usage of this API endpoint, please create an issue in this repository.\n\n## How to use\n\nInstall the package via:\n\n`pip install solmate-sdk`\n\nImport the `SolMateAPIClient` class and connect to your SolMate:\n\n```python\nfrom solmate_sdk import SolMateAPIClient\n\nclient = SolMateAPIClient("serial_num")\nclient.connect()\nprint(f"Your SolMate online status is: {client.check_online()}")\n\n# or for the protected API:\nclient.quickstart()\nprint(client.get_live_values())\n```\n\nThe SolMate SDK communicates via a Websocket API with your SolMate.\n\n## Roadmap\n\n- Quickstart supports multiple serial numbers\n- Publish docs on Read The Docs\n- More Examples\n- Full Unit Testing\n- Car Charger Example\n\n## Links\n\n- Our Homepage [www.eet.energy](https://www.eet.energy)\n- The project on PyPi [pypi.org/project/solmate-sdk](https://pypi.org/project/solmate-sdk/)\n',
    'author': 'EET',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eet-energy/solmate-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

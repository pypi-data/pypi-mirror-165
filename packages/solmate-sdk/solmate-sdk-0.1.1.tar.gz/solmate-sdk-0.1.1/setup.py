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
    'version': '0.1.1',
    'description': 'Software Development Kit for the EET SolMate',
    'long_description': '# EET SolMate SDK\n\nAll you need to integrate your [EET](https://www.eet.energy) SolMate into your home automation system and any python based system. \nKeep in mind that this is **work in progress**.\n\nThis python based SDK provides a class based API Client which let you:\n\n1. Login to your SolMate with serial number and password which returns an authentification token.\n2. Connect to your SolMate with the authentification token.\n3. Get live values of your SolMate.\n4. Check if your SolMate is online.\n\n## How to use\n\nInstall the package via:\n\n`pip install solmate-sdk`\n\nImport the `SolMateAPIClient` class and connect to your SolMate:\n\n```python\nfrom solmate_sdk.apiclient import SolMateAPIClient\n\nclient = SolMateAPIClient("serial_num")\nclient.connect()\nprint(f"Your SolMate online status is: {client.check_online()}")\n```\n\n## Implementation Details\n\nThe SolMate SDK communicate over the SolMate Websocket API with your SolMate.\n\n## Links\n\n- [www.eet.energy](https://www.eet.energy)\n- [pypi.org/project/solmate-sdk](https://pypi.org/project/solmate-sdk/)',
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

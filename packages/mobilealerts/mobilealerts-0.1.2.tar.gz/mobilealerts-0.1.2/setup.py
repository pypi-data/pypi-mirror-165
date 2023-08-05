# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mobilealerts']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8,<4.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=4.5.0,<5.0.0']}

setup_kwargs = {
    'name': 'mobilealerts',
    'version': '0.1.2',
    'description': 'Python classes for MobileAlerts gateway and sensors',
    'long_description': '# python-mobilealerts\n\n[![build](https://github.com/PlusPlus-ua/python-mobilealerts/actions/workflows/build.yml/badge.svg)](https://github.com/PlusPlus-ua/python-mobilealerts/actions/workflows/build.yml) [![Python Version](https://img.shields.io/pypi/pyversions/mobilealerts.svg)](https://pypi.org/project/mobilealerts/) [![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/PlusPlus-ua/python-mobilealerts/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit) [![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/PlusPlus-ua/python-mobilealerts/blob/master/.pre-commit-config.yaml) [![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/PlusPlus-ua/python-mobilealerts/releases) [![License](https://img.shields.io/github/license/PlusPlus-ua/python-mobilealerts)](https://github.com/PlusPlus-ua/python-mobilealerts/blob/master/LICENSE)\n\n\n## Python classes for MobileAlerts gateway and sensors\n\nLibrary act as proxy server which intercepts all measurements and sensors properties which sends MobileAlerts gateway to the cloud. \n\nEverything works in asynchronous way in order to build on the base of this library [Home assistant](https://github.com/home-assistant/core) integration.\n\n## Installation\n\n```bash\npip install -U python-mobilealerts\n```\n\nor install with `Poetry`\n\n```bash\npoetry add python-mobilealerts\n```\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/PlusPlus-ua/python-mobilealerts)](https://github.com/PlusPlus-ua/python-mobilealerts/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/PlusPlus-ua/python-mobilealerts/blob/master/LICENSE) for more details.\n\n## Credits\n\nThis project was inspired and developed on the base of [MMMMobileAlerts](https://github.com/sarnau/MMMMobileAlerts)\n\nThis project was generated with [python-package-template](https://github.com/TezRomacH/python-package-template)\n',
    'author': 'PlusPlus-ua',
    'author_email': 'alexplas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PlusPlus-ua/python-mobilealerts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

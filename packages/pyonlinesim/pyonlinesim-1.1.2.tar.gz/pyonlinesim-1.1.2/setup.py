# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyonlinesim',
 'pyonlinesim.clients',
 'pyonlinesim.core',
 'pyonlinesim.core.abc',
 'pyonlinesim.core.methods',
 'pyonlinesim.exceptions',
 'pyonlinesim.exceptions.rent',
 'pyonlinesim.exceptions.sms',
 'pyonlinesim.types',
 'pyonlinesim.types.rent',
 'pyonlinesim.types.sms']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3', 'pydantic>=1.9.2,<2.0.0']

setup_kwargs = {
    'name': 'pyonlinesim',
    'version': '1.1.2',
    'description': 'Asynchronous wrapper to interact with onlinesim.ru API',
    'long_description': '[![Downloads](https://pepy.tech/badge/pyonlinesim)](https://pepy.tech/project/pyonlinesim)\n[![Downloads](https://pepy.tech/badge/pyonlinesim/month)](https://pepy.tech/project/pyonlinesim)\n[![Downloads](https://pepy.tech/badge/pyonlinesim/week)](https://pepy.tech/project/pyonlinesim)\n[![Code Quality Score](https://api.codiga.io/project/34377/score/svg)](https://api.codiga.io/project/34377/score/svg)\n[![Code Grade](https://api.codiga.io/project/34377/status/svg)](https://api.codiga.io/project/34377/status/svg)\n\n## 🔗 Links\n* 🎓 **Documentation:** [*CLICK*](https://pyonlinesim.readthedocs.io/en/latest/)\n* 🖱️ **Developer contacts:** [![Dev-Telegram](https://img.shields.io/badge/Telegram-blue.svg?style=flat-square&logo=telegram)](https://t.me/marple_tech)\n## 🐦 Dependencies  \n\n| Library  |                       Description                       |\n|:--------:|:-------------------------------------------------------:|\n| aiohttp  | Asynchronous HTTP Client/Server for asyncio and Python. |\n| pydantic |                   JSON Data Validator                   |\n\n---\n',
    'author': 'Marple',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marple-git/pyonlinesim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

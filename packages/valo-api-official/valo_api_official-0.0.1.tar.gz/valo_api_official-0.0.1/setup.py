# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['valo_api_official',
 'valo_api_official.endpoints',
 'valo_api_official.exceptions',
 'valo_api_official.responses',
 'valo_api_official.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'valo-api-official',
    'version': '0.0.1',
    'description': 'Valorant API Wrapper',
    'long_description': '# valo_api_official\n\n<div align="center">\n\n[![Build status](https://github.com/raimannma/ValorantAPIOfficial/workflows/build/badge.svg?branch=master&event=push)](https://github.com/raimannma/ValorantAPIOfficial/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/valo_api_official.svg)](https://pypi.org/project/valo_api/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/raimannma/ValorantAPI/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/raimannma/ValorantAPIOfficial/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/raimannma/ValorantAPIOfficial/releases)\n[![License](https://img.shields.io/github/license/raimannma/ValorantAPIOfficial)](https://github.com/raimannma/ValorantAPIOfficial/blob/master/LICENSE)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/3b23d2a3b1694356bc95255a2edb83e6)](https://www.codacy.com/gh/raimannma/ValorantAPIOfficial/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=raimannma/ValorantAPIOfficial&amp;utm_campaign=Badge_Grade)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/3b23d2a3b1694356bc95255a2edb83e6)](https://www.codacy.com/gh/raimannma/ValorantAPIOfficial/dashboard?utm_source=github.com&utm_medium=referral&utm_content=raimannma/ValorantAPIOfficial&utm_campaign=Badge_Coverage)\n[![Downloads](https://pepy.tech/badge/valo-api-official)](https://pepy.tech/project/valo-api-official)\n\nValorant API Wrapper\n\n</div>\n\n## Installation\n\n    pip install valo-api\n\n## Documentation\n\n### Hosted\n\nThe documentation is hosted here: https://raimannma.github.io/ValorantAPIOfficial/\n\n### From Source\n\nAfter installing the package dependencies `pip install -r requirements.txt`, you can use the following commands to get the documentation:\n\n    cd docs/ && make html\n\nOpen the index.html file in the docs/_build/html/ directory.\n',
    'author': 'Manuel Raimann',
    'author_email': 'raimannma@outlook.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/raimannma/ValorantAPIOfficial',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

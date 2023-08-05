# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['syngo', 'syngo.migrations']

package_data = \
{'': ['*'], 'syngo': ['templates/syngo/*']}

install_requires = \
['Django>=3.2,<4.0', 'captcha>=0.4,<0.5', 'httpx>=0.23.0,<0.24.0']

setup_kwargs = {
    'name': 'syngo',
    'version': '0.2.0',
    'description': 'Manage Synapse from Django',
    'long_description': '# SynGo\n\n[![Tests](https://github.com/nim65s/syngo/actions/workflows/test.yml/badge.svg)](https://github.com/nim65s/syngo/actions/workflows/test.yml)\n[![Lints](https://github.com/nim65s/syngo/actions/workflows/lint.yml/badge.svg)](https://github.com/nim65s/syngo/actions/workflows/lint.yml)\n[![Release](https://github.com/nim65s/syngo/actions/workflows/release.yml/badge.svg)](https://pypi.org/project/syngo/)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/nim65s/syngo/main.svg)](https://results.pre-commit.ci/latest/github/nim65s/syngo/main)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![codecov](https://codecov.io/gh/nim65s/syngo/branch/main/graph/badge.svg?token=BLGISGCYKG)](https://codecov.io/gh/nim65s/syngo)\n[![Maintainability](https://api.codeclimate.com/v1/badges/a0783da8c0461fe95eaf/maintainability)](https://codeclimate.com/github/nim65s/syngo/maintainability)\n[![PyPI version](https://badge.fury.io/py/syngo.svg)](https://badge.fury.io/py/syngo)\n\nManage Synapse from Django\n\n## Install\n\n```\npython3 -m pip install syngo\n```\n\n## Unit tests\n\n```\ndocker-compose -f test.yml up --exit-code-from tests --force-recreate --build\n```\n',
    'author': 'Guilhem Saurel',
    'author_email': 'guilhem.saurel@laas.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nim65s/syngo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

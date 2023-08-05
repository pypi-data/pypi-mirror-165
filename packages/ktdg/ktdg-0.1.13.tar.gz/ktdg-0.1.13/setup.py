# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ktdg']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.0,<2.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['ktdg = ktdg.cli:run_cli']}

setup_kwargs = {
    'name': 'ktdg',
    'version': '0.1.13',
    'description': 'Library to simulate knowledge tracing datasets',
    'long_description': '[![Pipeline](https://gitlab.com/antoinelb/ktdg/badges/main/pipeline.svg)](https://gitlab.com/antoinelb/ktdg/commits/main)\n[![coverage report](https://gitlab.com/antoinelb/ktdg/badges/main/coverage.svg)](https://gitlab.com/antoinelb/ktdg/commits/main)\n[![Pypi version](https://img.shields.io/pypi/v/ktdg)](https://pypi.org/project/ktdg/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n[![security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n\n# ktdg (Knowledge tracing data generator)\n\nLibrary used to create synthetic knowledge tracing data.\nExample configs can be found in `config`.\n\n[__Usage__](#usage)\n| [__Setup__](#setup)\n| [__Documentation__](#documentation)\n\n## Usage\n\nTo create a new config or complete an existing one:\n\n```\n$ ktdg create --help\nUsage: ktdg create [OPTIONS] CONFIG\n\n  (c) Creates a config or completes it, saving it to the given file.\n\nArguments:\n  CONFIG  Path of the config to complete or create  [required]\n\nOptions:\n  -h, --help  Show this message and exit.\n```\n\nTo generate the synthetic data from the config:\n\n```\n$ ktdg generate --help\nUsage: ktdg generate [OPTIONS] CONFIG\n\n  (g) Generates the data for the given config, saving it as a json file named\n  "data.json".\n\nArguments:\n  CONFIG  Configuration file to use  [required]\n\nOptions:\n  -h, --help  Show this message and exit.\n```\n\n## Setup\n\n1. Install [`poetry`](https://github.com/python-poetry/poetry)\n\n2. `poetry config virtualenvs.in-project true`\n\n3. `poetry install`\n\n4. `source .venv/bin/activate`\n\n## Documentation\n\n### Distributions\n\n__constant__: All samples have the same value `value`.\n\n__normal__: Samples are taken from a normal distribution with mean `mu` and standard deviation `sigma`.\n\n__binomial__: Samples are taken from a binomial distribution with number of possible successes `n` and probability of success `p`.\n',
    'author': 'Antoine Lefebvre-Brossard',
    'author_email': 'antoinelb@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/antoinelb/ktdg',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)

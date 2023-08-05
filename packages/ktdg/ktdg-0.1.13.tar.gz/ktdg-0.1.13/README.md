[![Pipeline](https://gitlab.com/antoinelb/ktdg/badges/main/pipeline.svg)](https://gitlab.com/antoinelb/ktdg/commits/main)
[![coverage report](https://gitlab.com/antoinelb/ktdg/badges/main/coverage.svg)](https://gitlab.com/antoinelb/ktdg/commits/main)
[![Pypi version](https://img.shields.io/pypi/v/ktdg)](https://pypi.org/project/ktdg/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)

# ktdg (Knowledge tracing data generator)

Library used to create synthetic knowledge tracing data.
Example configs can be found in `config`.

[__Usage__](#usage)
| [__Setup__](#setup)
| [__Documentation__](#documentation)

## Usage

To create a new config or complete an existing one:

```
$ ktdg create --help
Usage: ktdg create [OPTIONS] CONFIG

  (c) Creates a config or completes it, saving it to the given file.

Arguments:
  CONFIG  Path of the config to complete or create  [required]

Options:
  -h, --help  Show this message and exit.
```

To generate the synthetic data from the config:

```
$ ktdg generate --help
Usage: ktdg generate [OPTIONS] CONFIG

  (g) Generates the data for the given config, saving it as a json file named
  "data.json".

Arguments:
  CONFIG  Configuration file to use  [required]

Options:
  -h, --help  Show this message and exit.
```

## Setup

1. Install [`poetry`](https://github.com/python-poetry/poetry)

2. `poetry config virtualenvs.in-project true`

3. `poetry install`

4. `source .venv/bin/activate`

## Documentation

### Distributions

__constant__: All samples have the same value `value`.

__normal__: Samples are taken from a normal distribution with mean `mu` and standard deviation `sigma`.

__binomial__: Samples are taken from a binomial distribution with number of possible successes `n` and probability of success `p`.

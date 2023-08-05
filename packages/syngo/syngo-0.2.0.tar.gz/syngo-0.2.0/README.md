# SynGo

[![Tests](https://github.com/nim65s/syngo/actions/workflows/test.yml/badge.svg)](https://github.com/nim65s/syngo/actions/workflows/test.yml)
[![Lints](https://github.com/nim65s/syngo/actions/workflows/lint.yml/badge.svg)](https://github.com/nim65s/syngo/actions/workflows/lint.yml)
[![Release](https://github.com/nim65s/syngo/actions/workflows/release.yml/badge.svg)](https://pypi.org/project/syngo/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/nim65s/syngo/main.svg)](https://results.pre-commit.ci/latest/github/nim65s/syngo/main)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/nim65s/syngo/branch/main/graph/badge.svg?token=BLGISGCYKG)](https://codecov.io/gh/nim65s/syngo)
[![Maintainability](https://api.codeclimate.com/v1/badges/a0783da8c0461fe95eaf/maintainability)](https://codeclimate.com/github/nim65s/syngo/maintainability)
[![PyPI version](https://badge.fury.io/py/syngo.svg)](https://badge.fury.io/py/syngo)

Manage Synapse from Django

## Install

```
python3 -m pip install syngo
```

## Unit tests

```
docker-compose -f test.yml up --exit-code-from tests --force-recreate --build
```

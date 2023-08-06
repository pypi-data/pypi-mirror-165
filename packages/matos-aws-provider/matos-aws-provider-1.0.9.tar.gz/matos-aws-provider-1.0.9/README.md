[![Unit Test](https://github.com/cloudmatos/matos-aws-provider/actions/workflows/matos-tox.yml/badge.svg?branch=develop)](https://github.com/cloudmatos/matos-aws-provider/actions/workflows/matos-tox.yml)
[![Pylint](https://github.com/cloudmatos/matos-aws-provider/actions/workflows/matos-pylint.yml/badge.svg?branch=develop)](https://github.com/cloudmatos/matos-aws-provider/actions/workflows/matos-pylint.yml)

# matos-aws-provider

The 'matos-aws-provider' is an open-source python package for developing security tools to identify threats in your Amazon Web Services (AWS) infrastructure. It uses the service providers Cloud SDK to deduce the current state and metadata of the underlying services.

# How to build
1. python -m pip install -U setuptools wheel build
2. python -m build .

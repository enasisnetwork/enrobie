# Enasis Network Chatting Robie

> :children_crossing: This project has not released its first major version.

Barebones service for connecting to multiple upstream chat networks.

[![](https://img.shields.io/github/actions/workflow/status/enasisnetwork/enrobie/build.yml?style=flat-square&label=GitHub%20actions)](https://github.com/enasisnetwork/enrobie/actions)<br>
[![codecov](https://img.shields.io/codecov/c/github/enasisnetwork/enrobie?token=7PGOXKJU0E&style=flat-square&logoColor=FFFFFF&label=Coverage)](https://codecov.io/gh/enasisnetwork/enrobie)<br>
[![](https://img.shields.io/readthedocs/enrobie?style=flat-square&label=Read%20the%20Docs)](https://enrobie.readthedocs.io)<br>
[![](https://img.shields.io/pypi/v/enrobie.svg?style=flat-square&label=PyPi%20version)](https://pypi.org/project/enrobie)<br>
[![](https://img.shields.io/pypi/dm/enrobie?style=flat-square&label=PyPi%20downloads)](https://pypi.org/project/enrobie)

## Documentation
Documentation is on [Read the Docs](https://enrobie.readthedocs.io).
Should you venture into the sections below you will be able to use the
`sphinx` recipe to build documention in the `docs/html` directory.

## Installing the package
Installing stable from the PyPi repository
```
pip install enrobie
```
Installing latest from GitHub repository
```
pip install git+https://github.com/enasisnetwork/enrobie
```

## Quick start for local development
Start by cloning the repository to your local machine.
```
git clone https://github.com/enasisnetwork/enrobie.git
```
Set up the Python virtual environments expected by the Makefile.
```
make -s venv-create
```

## Version management
:warning: Ensure that no changes are pending.

1. Rebuild the environment.
   ```
   make -s check-revenv
   ```

1. Update the [version.txt](enrobie/version.txt) file.

1. Push to the `main` branch.

1. Create [repository](https://github.com/enasisnetwork/enrobie) release.

1. Build the Python package.<br>Be sure no uncommited files in tree.
   ```
   make -s pypackage
   ```

1. Upload Python package to PyPi test.
   ```
   make -s pypi-upload-test
   ```

1. Upload Python package to PyPi prod.
   ```
   make -s pypi-upload-prod
   ```

1. Update [Read the Docs](https://enrobie.readthedocs.io) documentation.

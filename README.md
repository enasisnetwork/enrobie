# Enasis Network Chatting Robie

> :warning: This project has not released its first major version.

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

### Execute the linters and tests
The comprehensive approach is to use the `check` recipe. This will stop on
any failure that is encountered.
```
make -s check
```
However you can run the linters in a non-blocking mode.
```
make -s linters-pass
```
And finally run the various tests to validate the code and produce coverage
information found in the `htmlcov` folder in the root of the project.
```
make -s pytest
```

## Running the service
There are several command line arguments, see them all here.
```
python -m enrobie.execution.service --help
```
Here is an example of running the service from inside the project folder
within the [Workspace](https://github.com/enasisnetwork/workspace) project.
```
python -m enrobie.execution.service \
  --config ../../Persistent/enrobie-prod.yml \
  --console \
  --debug \
  --print_command
```
Replace `../../Persistent/enrobie-prod.yml` with your configuration file.

## Deploying the service
It is possible to deploy the project with the Ansible roles located within
the [Orchestro](https://github.com/enasisnetwork/orchestro) project! Below
is an example of what you might run from that project to deploy this one.
However there is a bit to consider here as this requires some configuration.
```
make -s \
  limit=all \
  orche_files=../../Persistent/orchestro-prod.yml \
  ansible_args=" --diff" \
  enrobie-install
```

## Version management
> :warning: Ensure that no changes are pending.

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

1. Consider running builds on dependent projects.

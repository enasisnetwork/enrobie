# Enasis Network Chatting Robie

> :warning: This project has not released its first major version.

Barebones service for connecting to multiple upstream chat networks.

<a href="https://pypi.org/project/enrobie"><img src="https://enasisnetwork.github.io/enrobie/badges/pypi.png"></a><br>
<a href="https://enasisnetwork.github.io/enrobie/validate/flake8.txt"><img src="https://enasisnetwork.github.io/enrobie/badges/flake8.png"></a><br>
<a href="https://enasisnetwork.github.io/enrobie/validate/pylint.txt"><img src="https://enasisnetwork.github.io/enrobie/badges/pylint.png"></a><br>
<a href="https://enasisnetwork.github.io/enrobie/validate/ruff.txt"><img src="https://enasisnetwork.github.io/enrobie/badges/ruff.png"></a><br>
<a href="https://enasisnetwork.github.io/enrobie/validate/mypy.txt"><img src="https://enasisnetwork.github.io/enrobie/badges/mypy.png"></a><br>
<a href="https://enasisnetwork.github.io/enrobie/validate/yamllint.txt"><img src="https://enasisnetwork.github.io/enrobie/badges/yamllint.png"></a><br>
<a href="https://enasisnetwork.github.io/enrobie/validate/pytest.txt"><img src="https://enasisnetwork.github.io/enrobie/badges/pytest.png"></a><br>
<a href="https://enasisnetwork.github.io/enrobie/validate/coverage.txt"><img src="https://enasisnetwork.github.io/enrobie/badges/coverage.png"></a><br>
<a href="https://enasisnetwork.github.io/enrobie/validate/sphinx.txt"><img src="https://enasisnetwork.github.io/enrobie/badges/sphinx.png"></a><br>

## Documentation
Read [project documentation](https://enasisnetwork.github.io/enrobie/sphinx)
built using the [Sphinx](https://www.sphinx-doc.org/) project.
Should you venture into the sections below you will be able to use the
`sphinx` recipe to build documention in the `sphinx/html` directory.

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

## Using the Ainswer plugin
These dependencies are not automatically installed but are required when
using the new `AinswerPlugin`. Install the following when using that.
- `pydantic-ai-slim`
- `pydantic-ai-slim[anthropic]`
- `pydantic-ai-slim[openai]`

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

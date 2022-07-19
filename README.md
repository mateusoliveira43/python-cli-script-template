# Python CLI script template

[![Continuos Integration](https://github.com/mateusoliveira43/python-cli-script-template/actions/workflows/ci.yml/badge.svg)](https://github.com/mateusoliveira43/python-cli-script-template/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mateusoliveira43_python-cli-script-template&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=mateusoliveira43_python-cli-script-template)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

- [Arquivo README em português](docs/README_PT.md)

Template to create Python command line interface scripts, using Python's standard library [argparse](https://docs.python.org/3/library/argparse.html).

Check the repository [Wiki](https://github.com/mateusoliveira43/python-cli-script-template/wiki) for more details.

# Example of use

The `example` folder and the `run_example.py` file are an example of use of the template.

To run the example, run
```
[python|python3] ./run_example.py
[python|python3] ./run_example.py -h
[python|python3] ./run_example.py --help
```
to display the example script's help message. Run the script with Python 3 command is optional.

# Docker

To connect to project's Docker container shell, run
```
docker/run.sh
```
It is not needed to have virtual environment active in the container.

To exit the container's shell, run `CTRL+D` or `exit`.

To run Dockerfile linter, run
```
docker/lint.sh
```

To remove the project's containers, images, volumes and networks, run
```
docker/down.sh
```

To change Docker configuration, change the variables in `.env` file.

# Quality

To run the template quality measures, it is needed to install its development requirements and have virtual environment active. To install then in a virtual environment, run
```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
```
or
```
poetry install
poetry shell
```
To deactivate virtual environment, run `CTRL+D` or `exit`.

The quality measures of the template are reproduced by the continuos integration (CI) pipeline of the project. CI configuration in `.github/workflows/ci.yml` file.

## Tests

To run tests and coverage report, run
```
pytest
```

To see the html report, check `tests/coverage-results/htmlcov/index.html`.

Tests and coverage configuration in `pyproject.toml` file.

## Type checking

To generate Python type files, run
```
stubgen --verbose --package cli --output .
```

To run Python type checker, run
```
mypy .
```

Python type checker configuration in `pyproject.toml` file.

## Linter

To run Python linter, run
```
prospector
```

Python linter configuration in `.prospector.yaml` file.

## Code formatters

To check Python code imports format, run
```
isort --check --diff .
```

To format Python code imports, run
```
isort .
```

To check Python code format, run
```
black --check --diff .
```

To format Python code, run
```
black .
```

isort and black configuration in `pyproject.toml` file.

To check all repository's files format, run
```
ec -verbose
```

File format configuration in `.editorconfig` file.

## Security vulnerability scanners

To check common security issues in Python code, run
```
bandit --recursive cli
bandit --recursive example
```

To check known security vulnerabilities in Python dependencies, run
```
safety check --file requirements/dev.txt --full-report
```

## SonarCloud Code Analysis

[SonarCloud](https://sonarcloud.io/) analyzes the source code of the project through the CI pipeline.

# Pre-commit

To configure pre-commit automatically when cloning the repo, run
```
pip install pre-commit
git config --global init.templateDir ~/.git-template
pre-commit init-templatedir --hook-type commit-msg --hook-type pre-commit ~/.git-template
```
Must be installed globally. More information in https://pre-commit.com/#automatically-enabling-pre-commit-on-repositories

To configure pre-commit locally, run
```
pip install pre-commit
pre-commit install --hook-type commit-msg --hook-type pre-commit
```
with your virtual environment active.

To test it, run
```
pre-commit run --all-files
```

# License

This repository is licensed under the terms of [MIT License](LICENSE).

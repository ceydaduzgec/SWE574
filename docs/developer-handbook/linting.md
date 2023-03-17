### Linting
Each commit must be linted. Pre-commit is currently configured for flake8, isort and black. So, please install the pre-commit linter hook by running the following command from the terminal you use `git`:

```
pip install pre-commit
pre-commit install
```
To manually run all pre-commit hooks on a repository:
```
pre-commit run --all-files
```
To update versions of pre-commit hooks to the latest version automatically:
```
pre-commit autoupdate
```
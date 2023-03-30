# Testing
1. Enter the interactive bash of the container by running `source tools/run_development.sh`
2. Run `python manage.py test`

**Note**: If you want to run tests with different settings configurations you can use ---settings option for example: `python manage.py --settings=PROJECT.settings.dev test`

## Coverage Report
[Use coverage.py](https://coverage.readthedocs.io/en/7.2.2/)

- Enter the interactive bash of the container by running `source tools/run_development.sh`
- Install coverage.py by running `pip install coverage`
- Run `coverage run manage.py test` or if you already have a test database:`coverage run manage.py test --keepdb`
- Run `coverage report` to see the report.
- For a nicer presentation, use `coverage html` to get annotated HTML listings detailing missed lines.Then open `htmlcov/index.html` in your browser.

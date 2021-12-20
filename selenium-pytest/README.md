# Web tests for test tasks
Web Tests for test tasks

The framework for automated tests based on the Selenium WebDriver and PyTest.
The installation of the tools requires Python 3.6
This should be installed in a virtualenv env and activated.

### Add path to PYTHONPATH variable
`export PYTHONPATH="$PYTHONPATH:/path/to/tests"`

### Installing libraries
`pip install -r selenium-pytest/scripts/requirements.txt`

### Changing config
Change the `configuration/config.py` or set `ENV`, `BROWSER` environment variables (`dev`, `chrome` by default).
Requires an installed browser.

### Run tests
`pytest -s selenium-pytest`

### Bash script for running tests (for CI)
Run this command from CI pipelines or locally in the console from the project directory:
`./selenium-pytest/scripts/setup_and_run_tests.sh`

The running script can be parametrized:
`./selenium-pytest/scripts/setup_and_run_tests.sh dev chrome`

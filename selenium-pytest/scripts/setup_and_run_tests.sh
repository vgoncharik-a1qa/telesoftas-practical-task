#!/bin/bash

python -VV; which python
export PYTHONPATH="$PYTHONPATH:${WORKSPACE}/telesoftas-practical-task.git/selenium-pytest"
export PYTHONPATH="$PYTHONPATH:${WORKSPACE}/selenium-pytest"
python -m pip install --upgrade pip setuptools wheel
pip install -r selenium-pytest/scripts/requirements.txt --progress-bar off

if [[ ! -z "$1" ]]; then
  echo "PARAM=$1"
  export ENV=$1
fi
if [[ ! -z "$2" ]]; then
  export BROWSER=$2
fi
if [[ -z "$3" ]]; then
  export HEADLESS=$3
fi
if [[ -z "$4" ]]; then
  export REMOTE=$4
fi
if [[ -z "$5" ]]; then
  export REMOTE_URL=$5
fi

if [[ "$6" == "ci" ]]; then
  echo "Running in CI mode"
  PARAMS=(-s -o junit_family=xunit2 --junitxml=pytest_results.xml "--alluredir=${WORKSPACE}/allure-results" -v -m "${7}")
else
  echo "Running in normal mode"
  PARAMS=(-s)
fi

echo "Running web tests:"
python -VV; which python; which pytest
pytest "${PARAMS[@]}"  --maxfail=5  selenium-pytest

# Pytest returns
# 0 if all is well
# 1 if tests ran ok but some failed
# Other codes if something went wrong
# https://docs.pytest.org/en/stable/usage.html
PYTEST_RETURN_CODE=$?
if [[ $PYTEST_RETURN_CODE -lt 2 ]]; then
  echo "Web tests finished"; exit 0;
else
  echo "Web tests did not run properly"; exit $PYTEST_RETURN_CODE;
fi

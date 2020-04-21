#!/usr/bin/env bash
docstring_details=cat<<EOF
       ./bin/run-test.sh       # run all testcases
skip=1 ./bin/run-test.sh       # skip pipenv sync ie reuse current .venv/
       ./bin/run-test.sh -n 2  # run in parallel of 2 threads if cpu supported; otherwise will be 1

skip=1 ./bin/run-test.sh -s tests/test_azure_storage_blob/test_quickstart.py::Test::test01_open_connection
#                        #run specific testcase        at this file           class test_method
EOF

SH=$(cd `dirname $BASH_SOURCE` && pwd)  # SH aka SCRIPT_HOME for xx ie executed script's containing folder

[[ -z $skip ]] && pipenv sync; PYTHONPATH="$SH/.." pipenv run pytest $@
# ensure package installed                        # run test        any extra params applied

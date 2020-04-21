#!/usr/bin/env bash
docstring_details=cat<<EOF
       ./bin/run-test.sh       # run all testcases
skip=1 ./bin/run-test.sh       # skip pipenv sync ie reuse current .venv/
       ./bin/run-test.sh -n 2  # parallel run in 2 threads
EOF

docstring_details=cat<<EOF
note='can replace "pipenv run pytest" by ./bin/run-test.sh'

pipenv run pytest  # run all testcases

pipenv run pytest -n 2
# run in parallel of 2 threads if cpu supported; otherwise will be 1

pipenv run pytest -s tests/test_azure_storage_blob/test_quickstart.py::Test::test03_upload_dummy_pdf
#                 #run specific testcase        at this file           class test_method
EOF

[[ -z $skippipeenvsync ]] || pipenv sync;        pipenv run pytest $@
# ensure package installed     # run test        any extra params applied

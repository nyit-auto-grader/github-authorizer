#!/usr/bin/env bash
python -m venv venv
. venv/bin/activate
pip install -U pip setuptools
pip install -r requirements.txt
rm -rf /tmp/auto-grader-build.zip
export HERE=```pwd```
cd venv/lib/python3.6/site-packages
zip -r9 /tmp/auto-grader-build.zip *
cd ${HERE}
zip -g /tmp/auto-grader-build.zip lambda_function.py
cp /tmp/auto-grader-build.zip github-authorizer.zip
deactivate
rm -rf venv

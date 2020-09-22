#!/usr/bin/env bash
set -euo pipefail

# Backend lint
echo "Running backend lint"
flake8 --ignore=E501,W503 --exclude=wsgi.py,scripts,migrations,__init__.py,node_modules,akvo/rsr/views/translations.py akvo/
# Need environ to be set before other imports, etc. So, ignore E402
flake8 --ignore=E501,E402,W503 akvo/scripts/
flake8 --ignore=E501,E402,W503 akvo/wsgi.py

# Frontend lint
echo "Running frontend lint"

pushd akvo/rsr/dir
npm install
npm run lint
popd

pushd akvo/rsr/spa
npm install
npm run lint
popd

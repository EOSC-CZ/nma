#!/bin/bash

set -e

OAREPO_VERSION="${OAREPO_VERSION:-11}"

BUILDER_VENV=.venv-builder
if test -d $BUILDER_VENV ; then
	rm -rf $BUILDER_VENV
fi

python3 -m venv $BUILDER_VENV
. $BUILDER_VENV/bin/activate
pip install -U setuptools pip wheel
pip install -U oarepo-model-builder
pip install -U oarepo-model-builder-ui
pip install -U oarepo-model-builder-multilingual

if test -d test-datacite ; then
  rm -rf test-datacite
fi

oarepo-compile-model ./tests/test-datacite.yaml --output-directory test-datacite -vvv \
      --include datacite="./tests/datacite_4.5.yaml" \
      --include datacite-datatypes="./tests/datacite_datatypes_4.5.yaml"

VENV=".venv"

if test -d $VENV ; then
  rm -rf $VENV
fi

python3 -m venv $VENV
. $VENV/bin/activate
pip install -U setuptools pip wheel

pip install "oarepo==${OAREPO_VERSION}.*"
pip install -e ".[tests]"
pip install langdetect
pip install -e test-datacite

pip install oarepo-oai-pmh-harvester
pip uninstall -y uritemplate
pip install uritemplate


invenio index destroy --force --yes-i-know || true

pytest tests
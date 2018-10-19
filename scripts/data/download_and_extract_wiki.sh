#!/bin/bash

WIKIDUMP_URL=${1}
WIKIEXTRACTOR=${2}
DATA_FOLDER="data"
WIKIDUMP_FILE="${DATA_FOLDER}/wikidump.bz2"

mkdir -p ${DATA_FOLDER}/wiki/json ${DATA_FOLDER}/wiki/csv

wget ${WIKIDUMP_URL} -O ${WIKIDUMP_FILE} --continue

python3 -m scripts.data.extract_wiki \
  --wikiextractor ${WIKIEXTRACTOR} \
  --dump_file ${WIKIDUMP_FILE} \
  --json_dir ${DATA_FOLDER}/wiki/json/ \
  --csv_dir ${DATA_FOLDER}/wiki/csv/

rm ${WIKIDUMP_FILE}

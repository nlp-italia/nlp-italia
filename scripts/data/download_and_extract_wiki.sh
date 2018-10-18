#!/bin/bash

WIKIDUMP=${1}
WIKIEXTRACTOR=${2}
DATA_FOLDER='data'

wget ${WIKIDUMP} --directory-prefix=${DATA_FOLDER}/

mkdir -p ${DATA_FOLDER}/wiki ${DATA_FOLDER}/wiki/json ${DATA_FOLDER}/wiki/csv

python3 -m scripts.data.extract_wiki \
  --wikiextractor ${WIKIEXTRACTOR} \
  --dump_file ${DATA_FOLDER}/itwiki-latest-pages-articles.xml.bz2 \
  --json_dir ${DATA_FOLDER}/wiki/json/ \
  --csv_dir ${DATA_FOLDER}/wiki/csv/

rm ${DATA_FOLDER}/itwiki-latest-pages-articles.xml.bz2

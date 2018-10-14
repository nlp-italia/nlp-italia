#!/bin/bash

WIKIDUMP=${1}
WIKIEXTRACTOR=${2}

wget ${WIKIDUMP} --directory-prefix=data/

if [ ! -d "data/wiki" ]; then
  mkdir data/wiki
fi

if [ ! -d "data/wiki/json" ]; then
  mkdir data/wiki/json
fi

if [ ! -d "data/wiki/csv" ]; then
  mkdir data/wiki/csv
fi

python3 -m scripts.data.extract_wiki \
  --wikiextractor ${WIKIEXTRACTOR} \
  --dump_file data/itwiki-latest-pages-articles.xml.bz2 \
  --json_dir data/wiki/json/ \
  --csv_dir data/wiki/csv/

rm data/itwiki-latest-pages-articles.xml.bz2

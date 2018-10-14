import argparse
import glob
import json
import multiprocessing
import os
import subprocess

import pandas as pd


def extractWiki(wikiextractor, jsonDir, nProc, dumpFile):
    process = (
        "python3 {0} --json --filter_disambig_pages --quiet"
        " --output {1} --bytes 100M --processes {2} {3}".format(
            wikiextractor, jsonDir, nProc, dumpFile))

    process = list(map(lambda x: x.strip(), process.split(" ")))
    subprocess.call(process)


def wikiToCsv(jsonDir, csvDir, nProc):
    def aux(jsonPath, csvDir):
        """Auxiliari function, it transforms one single JSON into one CSV"""
        df = pd.DataFrame()
        with open(jsonPath, 'r') as fp:
            for line in fp:
                df = df.append(json.loads(line), ignore_index=True)
        filename = jsonPath.split("/")[-1].strip(".json")
        csvPath = os.path.join(csvDir, "{0}.tsv".format(filename))
        df.to_csv(csvPath, sep="\t")

    allJsons = glob.glob(os.path.join(jsonDir, "*"))
    nProc = min(len(allJsons), nProc)
    for i in range(0, len(allJsons), nProc):
        procs = []
        for j in range(nProc):
            index = i + j
            if index > len(allJsons):
                break

            jsonPath = allJsons[index]
            process = multiprocessing.Process(
                name=jsonPath, target=aux, args=(jsonPath, csvDir))
            procs.append(process)
            process.start()
        for proc in procs:
            proc.join()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--wikiextractor", type=str, help="Path to WikiExtractor.py file")
    parser.add_argument(
        '--dump_file', type=str, help="The wikipedia xml dumps"
        " Can be downloaded from https://dumps.wikimedia.org/")
    parser.add_argument(
        "--json_dir", type=str, help="Output for path wikiextractor, it will"
        " generate several files of fixed size. Each row of this files is a"
        " json string containing one article")
    parser.add_argument(
        "--csv_dir", type=str, default="", help="If not empy, each"
        " json file from wikiextractor will be converted into a csv")
    parser.add_argument(
        "--num_process", type=int, default=-1,
        help="Number of processes to use")
    args = parser.parse_args()

    nProc = args.num_process if args.num_process else \
        multiprocessing.cpu_count()

    extractWiki(args.wikiextractor, args.json_dir, nProc, args.dump_file)

    if args.csv_dir:
        wikiToCsv(args)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import sys

if not sys.version_info >= (3, 10):
    sys.exit("Need Python 3.10 or later.")

import argparse
from pathlib import Path
from importer import ResultsImporter
from ranker import Ranker


def main():
    parser = argparse.ArgumentParser(description="Calculate USARA Power Rankings.")
    parser.add_argument(
        "--json",
        metavar="path-to-output",
        type=Path,
        default="ranking_output_web/ranking_data.js",
        help="Path output ranking JSON to create.",
    )
    parser.add_argument(
        "path", metavar="path-to-data", type=Path, help="Path to data files."
    )

    args = parser.parse_args()

    ranker = Ranker()
    importer = ResultsImporter(ranker)

    data_files = [f for f in args.path.glob("*.xlsx") if f.is_file()]
    for f in data_files:
        importer.import_file(f)

    ranker.assign_rank()
    ranker.export_json(args.json)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import sys

if not sys.version_info >= (3, 10):
    sys.exit("Need Python 3.10 or later.")

import argparse
from pathlib import Path
from importer import ResultsImporter


def main():
    parser = argparse.ArgumentParser(description="Calculate USARA Power Rankings.")
    parser.add_argument(
        "path", metavar="path-to-data", type=Path, help="Path to data files."
    )

    args = parser.parse_args()

    importer = ResultsImporter()

    data_files = [f for f in args.path.iterdir() if f.is_file()]
    for f in data_files:
        importer.import_file(f)


if __name__ == "__main__":
    main()

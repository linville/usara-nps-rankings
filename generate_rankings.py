#!/usr/bin/env python3

import sys

if not sys.version_info >= (3, 10):
    sys.exit("Need Python 3.10 or later.")

import argparse
from pathlib import Path
from importer import ResultsImporter
from team_ranker import TeamRanker
from individual_ranker import IndividualRanker


def main():
    parser = argparse.ArgumentParser(description="Calculate USARA Power Rankings.")
    parser.add_argument(
        "--team-json",
        metavar="path-to-output",
        type=Path,
        default="ranking_output_web/team_ranking_data.js",
        help="Path output team ranking JSON to create.",
    )
    parser.add_argument(
        "--individual-json",
        metavar="path-to-output",
        type=Path,
        default="ranking_output_web/individual_ranking_data.js",
        help="Path output individual ranking JSON to create.",
    )
    parser.add_argument(
        "path", metavar="path-to-data", type=Path, help="Path to data files."
    )

    args = parser.parse_args()

    team_ranker = TeamRanker()
    indiv_ranker = IndividualRanker()
    importer = ResultsImporter(team_ranker, indiv_ranker)

    data_files = [f for f in args.path.glob("*.xlsx") if f.is_file()]
    for f in data_files:
        importer.import_file(f)

    team_ranker.assign_rank()
    team_ranker.export_json(args.team_json)

    indiv_ranker.assign_rank()
    indiv_ranker.export_json(args.individual_json)


if __name__ == "__main__":
    main()

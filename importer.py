import json
import tomllib


class ResultsImporter(object):
    def __init__(self, ranker):
        self._ranker = ranker

    @property
    def division_results(self):
        return self._division_results

    def import_file(self, path):
        print("Importing ", path)

        if path.suffix == ".json":
            with open(path, "r") as f:
                self._import_race(json.load(f))
        elif path.suffix == ".toml":
            with open(path, "rb") as f:
                self._import_race(tomllib.load(f))
        else:
            raise ValueError("Unknown file type: ", path)

    def _import_race(self, race_data):
        race_name = race_data["name"].strip()

        for ranking in race_data["rankings"]:
            self._import_ranking(race_data, ranking)

    def _import_ranking(self, race_data, ranking):
        race_name = race_data["name"]

        division = ranking["division"]
        team_name = ranking["team name"]
        overall_place = ranking["overall place"]
        division_place = ranking["division place"]
        members = None  # ranking["members"]

        points = 1

        self._ranker.add_entry(
            division,
            team_name,
            race_name,
            overall_place,
            overall_place,
            points,
            members,
        )

import json
import tomllib

class ResultsImporter(object):
    def __init__(self):
        self._division_results = {
            "C-3/4",
            "F-3/4",
            "M-3/4",
        }

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
        race_name = race_data["name"])
        

    def _add_entry(self, division, team_name, race_name, overall_rank, division_rank, points, members):
        pass
import math


def calc_max_race_points_from_length(length):
    if length <= 7:
        return 25
    elif length > 7 and length <= 15:
        return 50
    elif length > 15 and length <= 36:
        return 100
    elif length > 36 and length <= 72:
        return 125
    elif length > 72:
        return 150


class Ranker(object):
    def __init__(self):
        self._division_results = {"C-3/4": {}, "F-3/4": {}, "M-3/4": {}}

    def add_entry(
        self,
        race_info,
        division,
        team_name,
        overall_place,
        division_place,
        members,
    ):
        """Adds a new team into the division results"""

        if division.startswith("FAM"):
            # Skip importing family divisions, for now.
            return
        elif division.endswith("-1"):
            # Skip importing soloists, for now.
            return
        elif division.endswith("-2"):
            # Skip importing 2-person teams, for now.
            return

        if division not in self._division_results:
            print(f"Unknown division: {division}")
            return

        # USARA points are awarded using the formula below. Non-DNF
        # teams are awarded at least 2 points (DNF is 1 point).
        if division_place == "DNF":
            points = 1
        else:
            max_points = calc_max_race_points_from_length(race_info["Race Length"])

            points = round(max_points * (1 - math.log(overall_place) * 0.24))
            points = max(points, 2)

        if team_name not in self._division_results[division]:
            self._division_results[division][team_name] = {
                "points": 0,
                "race_data": [],
            }

        team_entry = self._division_results[division][team_name]
        team_entry["division"] = division
        team_entry["points"] += points

        team_entry["race_data"].append({
            "date": race_info["Race Date"].strftime("%Y-%m-%d"),
            "name": race_info["Race Name"],
            "overall": overall_place,
            "division": division_place,
            "points": points,
            "members": ", ".join(members),
        })

    def export_json(self, path_to_json):
        with open(path_to_json, "w") as f:
            f.write("var ranking_data = [\n")

            for division, results in self._division_results.items():
                for team, data in results.items():
                    f.write(
                        "  {\n"
                        f'    "rank": 0,\n'
                        f"    \"points\": {data['points']},\n"
                        f'    "team": "{team}",\n'
                        f"    \"total_races\": {len(data['race_data'])},\n"
                        f"    \"division\": \"{data['division']}\",\n"
                        f"    \"race_data\": {data['race_data']},\n"
                        "  },\n"
                    )
            f.write("];\n")

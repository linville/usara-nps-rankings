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
        # fmt: off
        self._division_results = {
            "C-3/4": {},
            "F-3/4": {},
            "M-3/4": {},
            "C-2": {},
            "F-2": {},
            "M-2": {},
            "F-1": {},
            "M-1": {},
        }
        # fmt: on

    def add_entry(
        self,
        race_info,
        division,
        team_name,
        overall_place,
        overall_count,
        division_place,
        division_count,
        members,
    ):
        """Adds a new team into the division results"""

        if division.startswith("FAM"):
            # Skip importing family divisions, for now.
            return

        if division not in self._division_results:
            print(f"Unknown division: {division}")
            return

        # USARA points are awarded using the formula below. Non-DNF
        # teams are awarded at least 2 points (DNF is 1 point).
        if overall_place == "DNF" or division_place == "DNF":
            points = 1
        else:
            max_points = calc_max_race_points_from_length(race_info["Race Length"])

            try:
                points = round(max_points * (1 - math.log(overall_place) * 0.24))
                points = max(points, 2)
            except TypeError as e:
                print(f"Invalid overall place: {overall_place}")

        if team_name not in self._division_results[division]:
            self._division_results[division][team_name] = {
                "rank": 0,
                "points": 0,
                "race_data": [],
            }

        team_entry = self._division_results[division][team_name]
        team_entry["division"] = division
        team_entry["points"] += points

        race_name_full = f"{race_info['Race Name']} {race_info['Race Length']} Hour"

        team_entry["race_data"].append({
            "date": race_info["Race Date"].strftime("%Y-%m-%d"),
            "name": race_name_full,
            "overall": overall_place,
            "overall_count": overall_count,
            "division": division_place,
            "division_count": division_count,
            "points": points,
            "members": ", ".join(members),
        })

    def assign_rank(self):
        for division, results in self._division_results.items():
            # Sort by points
            sorted_teams = sorted(
                results.items(), key=lambda x: x[1]["points"], reverse=True
            )

            sorted_teams[0][1]["rank"] = 1
            last_points = sorted_teams[0][1]["points"]

            rank = 0
            skip_rank = 0
            for team, data in sorted_teams[1:]:
                if data["points"] == last_points:
                    skip_rank += 1
                elif data["points"] < last_points:
                    rank += 1 + skip_rank
                    skip_rank = 0

                data["rank"] = rank + 1
                last_points = data["points"]

    def assign_totals(self):
        """This calculates the overall and division totals"""

    def export_json(self, path_to_json):
        with open(path_to_json, "w") as f:
            f.write("// You race, code and now you want data? Join us: http://github.com/linville/usara-nps-rankings\n\n")
            f.write("var ranking_data = [\n")

            for division, results in self._division_results.items():
                for team, data in results.items():
                    f.write(
                        "  {\n"
                        f"    \"rank\": {data['rank']},\n"
                        f"    \"points\": {data['points']},\n"
                        f'    "team": "{team}",\n'
                        f"    \"total_races\": {len(data['race_data'])},\n"
                        f"    \"division\": \"{data['division']}\",\n"
                        f"    \"race_data\": {data['race_data']},\n"
                        "  },\n"
                    )
            f.write("];\n")

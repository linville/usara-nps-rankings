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


class IndividualRanker(object):
    def __init__(self):
        self._usara_divisions = {
            "C-3/4": {},
            "F-3/4": {},
            "M-3/4": {},
            "C-2": {},
            "F-2": {},
            "M-2": {},
            "F-1": {},
            "M-1": {},
        }
        self._racer_results = {}


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

        if division not in self._usara_divisions:
            # Skip importing unknown divisions, for now.
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

        for racer in members:
            if racer not in self._racer_results:
                self._racer_results[racer] = {
                    "rank": 0,
                    "points": 0,
                    "race_data": [],
                }

            racer_entry = self._racer_results[racer]
            racer_entry["points"] += points

            race_name_full = f"{race_info['Race Name']} {race_info['Race Length']} Hour"

            racer_entry["race_data"].append({
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
        # Sort by points
        sorted_racers = sorted(
            self._racer_results.items(), key=lambda x: x[1]["points"], reverse=True
        )

        sorted_racers[0][1]["rank"] = 1
        last_points = sorted_racers[0][1]["points"]

        rank = 0
        skip_rank = 0
        for racer, data in sorted_racers[1:]:
            if data["points"] == last_points:
                skip_rank += 1
            elif data["points"] < last_points:
                rank += 1 + skip_rank
                skip_rank = 0

            data["rank"] = rank + 1
            last_points = data["points"]

    def export_json(self, path_to_json):
        with open(path_to_json, "w") as f:
            f.write("// You race, code and now you want data? Join us: http://github.com/linville/usara-nps-rankings\n\n")
            f.write("var ranking_data = [\n")

            for racer, data in self._racer_results.items():
                f.write(
                    "  {\n"
                    f"    \"rank\": {data['rank']},\n"
                    f"    \"points\": {data['points']},\n"
                    f'    "racer": "{racer}",\n'
                    f"    \"total_races\": {len(data['race_data'])},\n"
                    f"    \"race_data\": {data['race_data']},\n"
                    "  },\n"
                )
            f.write("];\n")

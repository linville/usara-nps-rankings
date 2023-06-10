class Ranker(object):
    def __init__(self):
        self._division_results = {
            "C-3/4": {},
            "F-3/4": {},
            "M-3/4": {}
        }

    def add_entry(
        self,
        division,
        team_name,
        race_name,
        race_date,
        overall_rank,
        division_rank,
        points,
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

        if team_name not in self._division_results[division]:
            self._division_results[division][team_name] = {
                "points": 0,
                "race_data": [],
            }

        team_entry = self._division_results[division][team_name]
        team_entry["division"] = division
        team_entry["points"] += points
        
        team_entry["race_data"].append({
            "date": race_date.strftime("%Y-%m-%d"),
            "name": race_name,
            "overall": overall_rank,
            "division": division_rank,
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

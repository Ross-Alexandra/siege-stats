from siege_stats.statistics_processing.stat_reader import StatReader
import os

if __name__ == "__main__":
    league_stats = StatReader()
    scrim_stats = StatReader()
    qualifier_stats = StatReader()
    total_stats = StatReader()

    league_path = os.path.join(os.getcwd(), *["resources", "league"])
    qualifier_path = os.path.join(os.getcwd(), *["resources", "qualifier"])
    scrim_path = os.path.join(os.getcwd(), *["resources", "scrim"])

    league_files = [os.path.join(league_path, f) for f in os.listdir(league_path) if os.path.isfile(os.path.join(league_path, f))]
    qualifier_files = [os.path.join(qualifier_path, f) for f in os.listdir(qualifier_path) if os.path.isfile(os.path.join(qualifier_path, f))]
    scrim_files = [os.path.join(scrim_path, f) for f in os.listdir(scrim_path) if os.path.isfile(os.path.join(scrim_path, f))]

    print(" ========== LEAGUE STATISTICS ========== ")
    if len(league_files) == 0:
        print("> No Data")
    else:
        for f in league_files:
            with open(f, "r") as league_file:
                league_stats.collect_match_performance(league_file)
        print(league_stats)

    print(" ========== QUALIFIER STATISTICS ========== ")
    if len(qualifier_files) == 0:
        print("> No Data")
    else:
        for f in qualifier_files:
            with open(f, "r") as qualifier_file:
                qualifier_stats.collect_match_performance(qualifier_file)
        print(qualifier_stats)

    print(" ========== SCRIM STATISTICS ========== ")
    if len(scrim_files) == 0:
        print("> No Data")
    else:
        for f in scrim_files:
            with open(f, "r") as scrim_file:
                scrim_stats.collect_match_performance(scrim_file)
        print(scrim_stats)

    print(" ========== AGGREGATE STATISTICS ========== ")
    if len(scrim_files) == 0 and len(qualifier_files) == 0 and len(league_files) == 0:
        print("> No Data")
    else:
        total_stats = scrim_stats + qualifier_stats + league_stats
        print(total_stats)
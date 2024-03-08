import pandas as pd
from rapidfuzz import process
from unidecode import unidecode

from fantasy_baseball import config


def fuzzy_match(name, names):
    matches = process.extract(name, names, score_cutoff=80)
    if len(matches) == 1:
        if matches[0][1] < 90:
            return name
        if matches[0][1] < 100:
            print(f"WARNING: Matching '{name}' to '{matches[0][0]}' with score {matches[0][1]}. Could be a problem.")
        return matches[0][0]
    elif len(matches) > 1:
        if matches[1][1] == 100:
            print(f"WARNING: Two identical matches for {name}!!!")
        if matches[0][1] >= 90:
            return matches[0][0]
    return name


def hitters():
    projections = pd.read_csv(config.DATA_DIRECTORY.joinpath("hitter_projections.csv"))
    projections = projections.rename(columns={"Name": "Player"})
    projections = projections.drop(columns=config.HIT_PROJ_DROP)
    # Remove any accent marks from player names for better matching
    projections["Player"] = projections["Player"].astype(str).apply(lambda x: unidecode(x))

    # Add TB to projections
    projections["TB"] = projections["H"] + (2 * projections["2B"]) + (3 * projections["3B"]) + (4 * projections["HR"])

    rankings = pd.read_csv(config.DATA_DIRECTORY.joinpath("hitter_rankings.csv"))
    rankings = rankings.drop(columns=config.HIT_RANK_DROP)
    # Remove any accent marks from player names for better matching
    rankings["Player"] = rankings["Player"].astype(str).apply(lambda x: unidecode(x))

    # Do our best to match names between the two data sets before merging
    player_names = rankings["Player"].tolist()
    projections["Player"] = projections["Player"].apply(lambda x: fuzzy_match(x, player_names))

    merge = pd.merge(projections, rankings, on="Player", how="left")
    rank_col = merge.pop("Rank")
    merge.insert(0, "Rank", rank_col)
    merge = merge.sort_values("Rank")

    for col in config.HIT_CATEGORIES:
        col_zscore = col + "_z"
        merge[col_zscore] = (merge[col] - merge[col].mean()) / merge[col].std(ddof=0)
        merge = merge.round({col_zscore: 2})

    merge["total_z"] = sum(merge[col + "_z"] for col in config.HIT_CATEGORIES)
    totalz_col = merge.pop("total_z")
    merge.insert(3, "total_z", totalz_col)

    merge.to_csv(config.DATA_DIRECTORY.joinpath("hitter.csv"), index=False)
    print("Hitter Z scores exported to sheets/hitter.csv")


def pitchers():
    projections = pd.read_csv(config.DATA_DIRECTORY.joinpath("pitcher_projections.csv"))
    projections = projections.rename(columns={"Name": "Player"})
    projections = projections.drop(columns=config.PITCH_PROJ_DROP)
    # Remove any accent marks from player names for better matching
    projections["Player"] = projections["Player"].astype(str).apply(lambda x: unidecode(x))

    rankings = pd.read_csv(config.DATA_DIRECTORY.joinpath("pitcher_rankings.csv"))
    rankings = rankings.drop(columns=config.PITCH_RANK_DROP)
    # Remove any accent marks from player names for better matching
    rankings["Player"] = rankings["Player"].astype(str).apply(lambda x: unidecode(x))

    # Do our best to match names between the two data sets before merging
    player_names = rankings["Player"].tolist()
    projections["Player"] = projections["Player"].apply(lambda x: fuzzy_match(x, player_names))

    merge = pd.merge(projections, rankings, on="Player", how="left")
    rank_col = merge.pop("Rank")
    merge.insert(0, "Rank", rank_col)
    merge = merge.sort_values("Rank")

    for col in config.PITCH_CAT_COUNT:
        col_zscore = col + "_z"
        merge[col_zscore] = (merge[col] - merge[col].mean()) / merge[col].std(ddof=0)
        merge = merge.round({col_zscore: 2})

    for col in config.PITCH_CAT_RATIO:
        col_zscore = col + "_z"
        merge[col_zscore] = -(merge[col] - merge[col].mean()) / merge[col].std(ddof=0)
        merge = merge.round({col_zscore: 2})

    # Intentionally excluding ER_z here
    merge["total_z"] = sum(merge[col + "_z"] for col in (config.PITCH_CAT_COUNT + config.PITCH_CAT_RATIO))
    totalz_col = merge.pop("total_z")
    merge.insert(3, "total_z", totalz_col)

    merge.to_csv(config.DATA_DIRECTORY.joinpath("pitcher.csv"), index=False)
    print("Hitter Z scores exported to sheets/pitcher.csv")


def main():
    config.load_config_file()
    hitters()
    pitchers()


if __name__ == "__main__":
    main()

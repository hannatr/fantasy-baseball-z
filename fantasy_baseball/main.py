import pandas as pd
from fuzzywuzzy import process


def fuzzy_match(name, names):
    match, threshold = process.extractOne(name, names)
    return match if threshold > 88 else name


def hitters():
    projections = pd.read_csv("sheets/hitter_projections.csv")
    projections = projections.rename(columns={"Name": "Player"})
    projections = projections.drop(
        columns=[
            "PA",
            "AB",
            "BB",
            "SO",
            "HBP",
            "CS",
            "-1",
            "OBP",
            "SLG",
            "wOBA",
            "wRC+",
            "-1.1",
            "WAR",
            "-1.2",
            "ADP",
            "-1.3",
            "playerid",
            "InterSD",
            "InterSK",
            "IntraSD",
        ]
    )
    # add TB to projections
    projections["TB"] = projections["H"] + projections["2B"] + (2 * projections["3B"]) + (3 * projections["HR"])

    rankings = pd.read_csv("sheets/hitter_rankings.csv")
    rankings = rankings.drop(
        columns=[
            "Team",
            "Positions",
            "Overall",
            "Best",
            "Worst",
            "Avg",
            "Std Dev",
            "ADP",
            "vs. ADP",
        ]
    )

    # Do our best to match names between the two data sets before merging
    player_names = list(
        filter(lambda x: isinstance(x, str), rankings["Player"].tolist())
    )
    projections["Player"] = projections["Player"].apply(
        lambda x: fuzzy_match(x, player_names)
    )

    merge = pd.merge(rankings, projections, on="Player")  # add how='left' to see differences
    merge = merge.sort_values("Rank")

    for col in ["H", "2B", "3B", "HR", "R", "RBI", "SB", "AVG", "OPS", "TB"]:
        col_zscore = col + "_z"
        merge[col_zscore] = (merge[col] - merge[col].mean()) / merge[col].std(ddof=0)
        merge = merge.round({col_zscore: 2})

    merge["total_z"] = sum(merge[col + "_z"] for col in ["H", "2B", "3B", "HR", "R", "RBI", "SB", "AVG", "OPS", "TB"])

    merge.to_csv("sheets/hitter.csv")
    print("Hitter Z scores exported to sheets/hitter.csv")
    print(merge)


def pitchers():
    projections = pd.read_csv("sheets/pitcher_projections.csv")
    projections = projections.rename(columns={"Name": "Player"})
    projections = projections.drop(
        columns=[
            "L",
            "G",
            "H",
            "HR",
            "BB",
            "BB/9",
            "FIP",
            "-1",
            "WAR",
            "RA9-WAR",
            "-1.1",
            "ADP",
            "-1.2",
            "playerid",
            "InterSD",
            "InterSK",
            "IntraSD",
        ]
    )

    rankings = pd.read_csv("sheets/pitcher_rankings.csv")
    rankings = rankings.drop(
        columns=[
            "Team",
            "Positions",
            "Overall",
            "Best",
            "Worst",
            "Avg",
            "Std Dev",
            "ADP",
            "vs. ADP",
        ]
    )

    # Do our best to match names between the two data sets before merging
    player_names = list(
        filter(lambda x: isinstance(x, str), rankings["Player"].tolist())
    )
    projections["Player"] = projections["Player"].apply(
        lambda x: fuzzy_match(x, player_names)
    )

    merge = pd.merge(rankings, projections, on="Player")  # add how='left' to see differences
    merge = merge.sort_values("Rank")

    for col in ["W", "SV", "HLD", "SO", "K/9", "QS"]:
        col_zscore = col + "_z"
        merge[col_zscore] = (merge[col] - merge[col].mean()) / merge[col].std(ddof=0)
        merge = merge.round({col_zscore: 2})

    for col in ["ERA", "ER", "WHIP"]:
        col_zscore = col + "_z"
        merge[col_zscore] = -(merge[col] - merge[col].mean()) / merge[col].std(ddof=0)
        merge = merge.round({col_zscore: 2})

    merge["total_z"] = sum(merge[col + "_z"] for col in ["W", "SV", "HLD", "ERA", "ER", "SO", "WHIP", "K/9", "QS"])

    merge.to_csv("sheets/pitcher.csv")
    print("Hitter Z scores exported to sheets/pitcher.csv")
    print(merge)


def main():
    hitters()
    pitchers()

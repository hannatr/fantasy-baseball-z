import pandas as pd
from rapidfuzz import process
from unidecode import unidecode


def fuzzy_match(name, names):
    # TODO handle multiple players with the same name (team as secondary)
    match, threshold, _ = process.extractOne(name, names)
    return match if threshold >= 80 else name


def hitters():
    projections = pd.read_csv("sheets/hitter_projections.csv")
    projections = projections.rename(columns={"Name": "Player"})
    # Remove any accent marks from player names for better matching
    projections["Player"] = projections["Player"].astype(str).apply(lambda x: unidecode(x))
    projections = projections.drop(
        columns=[
            "#",
            "PA",
            "AB",
            "BB",
            "SO",
            "HBP",
            "CS",
            "BB%",
            "K%",
            "ISO",
            "BABIP",
            "OBP",
            "SLG",
            "wOBA",
            "wRC+",
            "ADP",
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
            "Overall",
            "Best",
            "Worst",
            "Avg",
            "Std Dev",
            "ADP",
            "vs. ADP",
        ]
    )
    # Remove any accent marks from player names for better matching
    rankings["Player"] = rankings["Player"].astype(str).apply(lambda x: unidecode(x))

    # Do our best to match names between the two data sets before merging
    player_names = rankings["Player"].tolist()
    projections["Player"] = projections["Player"].apply(lambda x: fuzzy_match(x, player_names))

    merge = pd.merge(projections, rankings, on="Player", how="left")
    rank_col = merge.pop("Rank")
    merge.insert(0, "Rank", rank_col)
    merge = merge.sort_values("Rank")

    for col in ["H", "2B", "3B", "HR", "R", "RBI", "SB", "AVG", "OPS", "TB"]:
        col_zscore = col + "_z"
        merge[col_zscore] = (merge[col] - merge[col].mean()) / merge[col].std(ddof=0)
        merge = merge.round({col_zscore: 2})

    merge["total_z"] = sum(merge[col + "_z"] for col in ["H", "2B", "3B", "HR", "R", "RBI", "SB", "AVG", "OPS", "TB"])
    totalz_col = merge.pop("total_z")
    merge.insert(3, "total_z", totalz_col)

    merge.to_csv("sheets/hitter.csv", index=False)
    print("Hitter Z scores exported to sheets/hitter.csv")
    print(merge)


def pitchers():
    projections = pd.read_csv("sheets/pitcher_projections.csv")
    projections = projections.rename(columns={"Name": "Player"})
    # Remove any accent marks from player names for better matching
    projections["Player"] = projections["Player"].astype(str).apply(lambda x: unidecode(x))
    projections = projections.drop(
        columns=[
            "#",
            "GS",
            "G",
            "L",
            "H",
            "HR",
            "BB",
            "BB/9",
            "K/BB",
            "HR/9",
            "AVG",
            "BABIP",
            "LOB%",
            "FIP",
            "ADP",
            "InterSD",
            "InterSK",
            "IntraSD",
        ]
    )

    rankings = pd.read_csv("sheets/pitcher_rankings.csv")
    rankings = rankings.drop(
        columns=[
            "Team",
            "Overall",
            "Best",
            "Worst",
            "Avg",
            "Std Dev",
            "ADP",
            "vs. ADP",
        ]
    )
    # Remove any accent marks from player names for better matching
    rankings["Player"] = rankings["Player"].astype(str).apply(lambda x: unidecode(x))

    # Do our best to match names between the two data sets before merging
    player_names = rankings["Player"].tolist()
    projections["Player"] = projections["Player"].apply(lambda x: fuzzy_match(x, player_names))

    merge = pd.merge(projections, rankings, on="Player", how="left")
    rank_col = merge.pop("Rank")
    merge.insert(0, "Rank", rank_col)
    merge = merge.sort_values("Rank")

    for col in ["W", "SV", "HLD", "SO", "K/9", "QS"]:
        col_zscore = col + "_z"
        merge[col_zscore] = (merge[col] - merge[col].mean()) / merge[col].std(ddof=0)
        merge = merge.round({col_zscore: 2})

    for col in ["ERA", "ER", "WHIP"]:
        col_zscore = col + "_z"
        merge[col_zscore] = -(merge[col] - merge[col].mean()) / merge[col].std(ddof=0)
        merge = merge.round({col_zscore: 2})

    # Intentionally excluding ER_z here
    merge["total_z"] = sum(merge[col + "_z"] for col in ["W", "SV", "HLD", "ERA", "SO", "WHIP", "K/9", "QS"])
    totalz_col = merge.pop("total_z")
    merge.insert(3, "total_z", totalz_col)

    merge.to_csv("sheets/pitcher.csv", index=False)
    print("Hitter Z scores exported to sheets/pitcher.csv")
    print(merge)


def main():
    hitters()
    pitchers()


if __name__ == "__main__":
    main()

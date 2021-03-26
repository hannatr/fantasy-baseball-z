=Custom Z Score Generator for Fantasy Baseball

I play in a fantasy baseball league with a lot of categories (20 total). To gain an edge, I wanted to find players that would do better in a 10x10 league when most rankings grade players based on the more common 5x5 format. So this script imports projection and ranking data and outputs a sheet with rankings fr each player as well as a total z score value for each player.

To run the script:

 - If you want to use the Python virtual environment, install poetry and run `poetry install`. You can then run the script using `poetry run python3 -m fantasy_baseball`.
 - Download a rankings spreadsheet you trust. I use FantasyPros: https://www.fantasypros.com/mlb/rankings/overall.php. Be sure to download pitcher and hitter rankings separately.
 - Download a projections spreadsheet you trust. I use ATC: https://www.fangraphs.com/projections.aspx?pos=all&stats=bat&type=atc. Be sure to download pitcher and hitter projections separately.
 - Update the file paths in `main.py` to your downloaded sheets.
 - The names between your rankings and projections probably don't match for all players. Add the `how='left'` flag to the two `pd.merge()` calls in main.py. Run the script. Manually examine the output files `sheets/hitters.csv` and `sheets/pitchers.csv` for names that don't match. Update your projections spreadsheet to match the rankings spreadsheet names.
 - Update the categories for your league in `main.py`.
 - Run the scripts and examine the outputted sheets.
 
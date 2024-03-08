import json
import pathlib

# Overwritten from config file!!!
# Do not import these directly (e.g., from config import HIT_CATEGORIES) to prevent race condition at startup!
HIT_CATEGORIES = []
HIT_PROJ_DROP = []
HIT_RANK_DROP = []
PITCH_CAT_COUNT = []
PITCH_CAT_RATIO = []
PITCH_PROJ_DROP = []
PITCH_RANK_DROP = []
# End overwritten from config file

# Non-config file configuration
APP_DIRECTORY = pathlib.Path(__file__).parent.parent.resolve()
DATA_DIRECTORY = APP_DIRECTORY.joinpath("data").resolve()
CONFIG_FILE = DATA_DIRECTORY.joinpath("config.json").resolve()  # Update to .json


def load_config_file() -> None:
    """Load config file and overwrite default values."""
    global HIT_CATEGORIES, HIT_PROJ_DROP, HIT_RANK_DROP, PITCH_CAT_COUNT, PITCH_CAT_RATIO, PITCH_PROJ_DROP
    global PITCH_RANK_DROP

    try:
        if not CONFIG_FILE.exists():
            raise FileNotFoundError("Could not find config file")

        # Use json.load to read the JSON file
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)

        # Accessing elements directly as lists
        HIT_CATEGORIES = config["hit_categories"]
        HIT_PROJ_DROP = config["hit_proj_drop"]
        HIT_RANK_DROP = config["hit_rank_drop"]
        PITCH_CAT_COUNT = config["pitch_categories_count"]
        PITCH_CAT_RATIO = config["pitch_categories_ratio"]
        PITCH_PROJ_DROP = config["pitch_proj_drop"]
        PITCH_RANK_DROP = config["pitch_rank_drop"]
    except (FileNotFoundError, KeyError, ValueError, TypeError) as e:
        print(f"Error reading config file {CONFIG_FILE}: {e}")
        raise e

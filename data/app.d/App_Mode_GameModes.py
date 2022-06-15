# The Deephaven/OpenDota game mode class creator
# This script runs in app mode

"""
This script defines the function that can be used to get the list of game modes.

If the parquet file of game mode data exists, it will read from that instead.

Usage:

get_dota2_game_modes()

The Dota2.GameModes class has three parts:
Dota2.GameModes.json - A list of dicts in JSON format, one for each game mode
Dota2.GameModes.dataframe - A Pandas DataFrame for game modes
Dota2.GameModes.table - A Deephaven table identical to the dataframe
"""

from deephaven import parquet as dhpq
from deephaven import pandas as dhp

import datetime, json, os, pandas as pd, requests

def get_dota2_gamemodes():
    global Dota2

    parquet_data_exists = False
    ls_parquet = os.listdir("/data/parquet")
    if any(["gamemodes" in item for item in ls_parquet]):
        parquet_data_exists = True
        for idx, file in enumerate(ls_parquet):
            if "gamemodes" in file:
                pq_fname = file

    if not(parquet_data_exists):

        print("No local game mode data found. Pulling from OpenDOTA.")

        resp = requests.get("https://api.opendota.com/api/constants/game_mode")

        if not(resp.status_code == 200):
            print("The request failed. There may be an outage.")
            return

        game_mode_json = resp.json()

        game_modes_json = []

        for item in game_mode_json:
            id = game_mode_json[item]["id"]
            name = " ".join(game_mode_json[item]["name"].split("_")[2:]).title()
            if not("balanced" in game_mode_json[item].keys()):
                balanced = False
            else:
                balanced = game_mode_json[item]["balanced"]
            game_modes_json.append({"ID": id, "Name": name, "Balanced": balanced})
        
        Dota2.GameModes.json = game_modes_json
        Dota2.GameModes.dataframe = pd.DataFrame(game_modes_json)
        Dota2.GameModes.table = dhp.to_table(Dota2.GameModes.dataframe)\
            .update(["ID = (int)ID", "Name = (java.lang.String)Name", "Balanced = (boolean)Balanced"])

        todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
        fname = f"/data/parquet/gamemodes_{todays_date}.parquet"
        dhpq.write(Dota2.GameModes.table, fname, compression_codec_name="GZIP")

    else:

        fname_write_date = pq_fname.split("_")[1].split(".")[0]
        print(f"Found local game mode data. It was written on {fname_write_date}.")

        Dota2.GameModes.table = dhpq.read(f"/data/parquet/{pq_fname}")
        Dota2.GameModes.dataframe = dhp.to_pandas(Dota2.GameModes.table)
        Dota2.GameModes.json = Dota2.GameModes.dataframe.to_dict("records")

get_dota2_gamemodes()
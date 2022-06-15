# The Deephaven/OpenDOTA Hero class creator
# This scripts runs in app mode

"""
This script defines the function that can be used to get the list of heroes and their attributes.

If the parquet file of hero data exists, it will read from that instead.

Usage:

get_dota2_heroes()

The Dota2.Heroes class has three parts:
Dota2.Heroes.json - A list of dicts in JSON format, one for each hero
Dota2.Heroes.dataframe - A Pandas DataFrame for heroes and attributes
Dota2.Heroes.table - A Deephaven table identical to the dataframe 
"""

from deephaven import parquet as dhpq
from deephaven import pandas as dhp

import datetime, json, os, pandas as pd, requests

def get_dota2_heroes():
    global Dota2

    parquet_data_exists = False
    ls_parquet = os.listdir("/data/parquet")
    if any(["heroes" in item for item in ls_parquet]):
        parquet_data_exists = True
        for idx, file in enumerate(ls_parquet):
            if "heroes" in file:
                pq_fname = file

    if not(parquet_data_exists):

        print("No local hero data found. Pulling from OpenDOTA.")

        resp = requests.get("https://api.opendota.com/api/heroes")

        if not(resp.status_code == 200):
            print("The request failed. There may be an outage.")
            return

        heroes_json = resp.json()

        Dota2.Heroes.json = heroes_json
        Dota2.Heroes.dataframe = pd.DataFrame(heroes_json)
        Dota2.Heroes.table = dhp.to_table(Dota2.Heroes.dataframe)\
            .update_view(["Roles = (java.lang.String[])jpy.array(`java.lang.String`, roles)", \
                "Name = (java.lang.String)name", "LocalizedName = (java.lang.String)localized_name", \
                "Attribute = (java.lang.String)primary_attr", "AttackType = (java.lang.String)attack_type", \
                "Legs = (int)legs"])\
            .drop_columns(["name", "localized_name", "primary_attr", "attack_type", "roles", "legs"])

        todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
        fname = f"/data/parquet/heroes_{todays_date}.parquet"
        dhpq.write(Dota2.Heroes.table, fname, compression_codec_name="GZIP")

    else:

        fname_write_date = pq_fname.split("_")[1].split(".")[0]
        print(f"Found local hero data. It was written on {fname_write_date}.")

        Dota2.Heroes.table = dhpq.read(f"/data/parquet/{pq_fname}")
        Dota2.Heroes.dataframe = dhp.to_pandas(Dota2.Heroes.table)
        Dota2.Heroes.dataframe["Roles"] = Dota2.Heroes.dataframe["Roles"].apply(lambda item: list(item))
        Dota2.Heroes.json = Dota2.Heroes.dataframe.to_dict("records")

get_dota2_heroes()
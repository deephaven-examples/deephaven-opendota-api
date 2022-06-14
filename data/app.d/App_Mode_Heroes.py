# The Deephaven/OpenDOTA Hero class creator
# This scripts runs in app mode

"""
This script defines the function that can be used to get the list of heroes and their attributes.
Usage:

get_dota2_heroes()

The Dota2.Heroes class has three parts:
Dota2.Heroes.json - A list of dicts in JSON format, one for each hero
Dota2.Heroes.dataframe - A Pandas DataFrame for heroes and attributes
Dota2.Heroes.table - A Deephaven table identical to the dataframe 
"""

from deephaven import pandas as dhp

import pandas as pd, requests

def get_dota2_heroes():
    global Dota2

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

get_dota2_heroes()
# The Deephaven/OpenDota item class creator
# This script runs in app mode

"""
This script defines the function that can be used to get the list of items.
Usage:

get_dota2_items()

The Dota2.Items class has three parts:
Dota2.Items.json - A list of dicts in JSON format, one for each game mode
Dota2.Items.dataframe - A Pandas DataFrame for game modes
Dota2.Items.table - A Deephaven table identical to the dataframe
"""

from deephaven import pandas as dhp

import pandas as pd, requests

def get_dota2_items():
    global Dota2

    resp = requests.get("https://api.opendota.com/api/constants/items")

    if not(resp.status_code == 200):
        print("The request failed. There may be an outage.")
        return

    item_json = resp.json()
    
    items = []

    for item_name in item_json:
        item = item_json[item_name]
        id = item["id"]
        try:
            name = item["dname"]
        except KeyError:
            name = "No Name"
        if "hint" in item.keys():
            tooltip = item["hint"]
        else:
            tooltip = ""
        img_url = item["img"]
        notes = item["notes"]
        try:
            if not(item["charges"]):
                charges = 0
            else:
                charges = item["charges"]
        except KeyError:
            charges = 0
        attrib = []
        if item["attrib"]:
            for bonus in item["attrib"]:
                if "footer" in bonus.keys():
                    # print(item["dname"])
                    # print(f"{bonus['header']}{str(bonus['value'])} {bonus['footer']}")
                    attrib.append(f"{bonus['header']}{str(bonus['value'])} {bonus['footer']}")
                else:
                    attrib.append(f"{bonus['header']}{str(bonus['value'])}")
        attrib = ", ".join(attrib)

        items.append({"ID": id, "Name": name, "Tooltip": tooltip, "Attributes": attrib, "Notes": notes, "ImageURL": img_url})

    Dota2.Items.json = items
    Dota2.Items.dataframe = pd.DataFrame(items)
    Dota2.Items.table = dhp.to_table(Dota2.Items.dataframe)\
        .update(["Name = (java.lang.String)Name", "Tooltip = (java.lang.String[])Tooltip", \
            "Attributes = (java.lang.String)Attributes", "Notes = (java.lang.String)Notes", \
            "ImageURL = (java.lang.String)Notes"])

get_dota2_items()
# The Deephaven/OpenDota item class creator
# This script runs in app mode

"""
This script defines the function that can be used to get the list of items.

If the parquet file of item data exists, it will read from that instead.

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

    parquet_data_exists = False
    ls_parquet = os.listdir("/data/parquet")
    if any(["items" in item for item in ls_parquet]):
        parquet_data_exists = True
        for idx, file in enumerate(ls_parquet):
            if "items" in file:
                pq_fname = file

    if not(parquet_data_exists):

        print("No local item data found. Pulling from OpenDOTA.")

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
                tooltip = "".join([thing for thing in item if not(thing.isspace())])
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
            .update(["Name = (java.lang.String)Name", "Tooltip = (java.lang.String)Tooltip", \
                "Attributes = (java.lang.String)Attributes", "Notes = (java.lang.String)Notes", \
                "ImageURL = (java.lang.String)ImageURL"])

        todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
        fname = f"/data/parquet/items_{todays_date}.parquet"
        dhpq.write(Dota2.Items.table, fname, compression_codec_name="GZIP")

    else:

        fname_write_date = pq_fname.split("_")[1].split(".")[0]
        print(f"Found local item data. It was written on {fname_write_date}.")

        Dota2.Items.table = dhpq.read(f"/data/parquet/{pq_fname}")
        Dota2.Items.dataframe = dhp.to_pandas(Dota2.Items.table)
        Dota2.Items.json = Dota2.Items.dataframe.to_dict("records")

get_dota2_items()

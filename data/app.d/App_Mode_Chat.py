# The Deephaven/OpenDota item class creator
# This script runs in app mode

"""
This script defines the function that can be used to get the list of chatwheel items.

If the parquet file of item data exists, it will read from that instead.

Usage:

get_dota2_chatwheel()

The Dota2.Chatwheel class has three parts:
Dota2.Chatwheel.json - A list of dicts in JSON format, one for each chatwheel option
Dota2.Chatwheel.dataframe - A Pandas DataFrame for chatwheel options
Dota2.Chatwheel.table - A Deephaven table identical to the dataframe
"""

from deephaven import pandas as dhp

import pandas as pd, requests

def get_dota2_chatwheel():
    global Dota2

    parquet_data_exists = False
    ls_parquet = os.listdir("/data/parquet")
    if any(["chatwheels" in item for item in ls_parquet]):
        parquet_data_exists = True
        for idx, file in enumerate(ls_parquet):
            if "chatwheel" in file:
                pq_fname = file

    if not(parquet_data_exists):

        print("No local chatwheel data found. Pulling from OpenDOTA.")

        resp = requests.get("https://api.opendota.com/api/constants/chat_wheel")

        if not(resp.status_code == 200):
            print("The request failed. There may be an outage.")
            return

        chatwheel_json = resp.json()

        chatwheel = []

        for chat in chatwheel_json:
            chatwheel_to_append = {"ID": None, "Name": None, "Label": None, "Message": None, "Image": None, "All_Chat": False, "Sound_Ext": None, "Badge_Tier": None}
            keys = [field.title() for field in chatwheel_json[chat]]
            if "Id" in keys:
                keys[keys.index("Id")] = keys[keys.index("Id")].upper()
            for key in keys:
                chatwheel_to_append[key] = chatwheel_json[chat][key.lower()]
            chatwheel.append(chatwheel_to_append)

        Dota2.Chatwheel.json = chatwheel
        Dota2.Chatwheel.dataframe = pd.DataFrame(chatwheel)
        Dota2.Chatwheel.table = dhp.to_table(Dota2.Chatwheel.dataframe)\
            .update(["ID = (int)ID", "Name = (java.lang.String)Name", "Label = (java.lang.String)Label", "Message = (java.lang.String)Message"])

        todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
        fname = f"/data/parquet/chatwheel_{todays_date}.parquet"
        dhpq.write(Dota2.Chatwheel.table, fname, compression_codec_name="GZIP")

    else:

        fname_write_date = pq_fname.split("_")[1].split(".")[0]
        print(f"Found local chatwheel data. It was written on {fname_write_date}.")

        Dota2.Chatwheel.table = dhpq.reqd(f"/data/parquet/{pq_fname}")
        Dota2.Chatwheel.dataframe = dhp.to_pandas(Dota2.Chatwheel.table)
        Dota2.Chatwheel.json = Dota2.Chatwheel.dataframe.to_dict("records")

get_dota2_chatwheel()
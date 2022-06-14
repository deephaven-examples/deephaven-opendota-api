from deephaven.time import millis_to_datetime, now
from deephaven import DynamicTableWriter
import deephaven.dtypes as dht

import threading
import requests
import time
import json
import sys

def game_mode_from_id(game_mode_id):
    global Dota2
    for game_mode in Dota2.GameModes.json:
        if game_mode["ID"] == game_mode_id:
            return game_mode["Name"]

num_pulls = 60

live_match_col_defs = \
    {
        "MatchID": dht.int_, "StartTime": dht.DateTime, "EndTime": dht.DateTime, "IsActive": dht.bool_, "LeagueID": dht.int_, "SeriesID": dht.int_, "AverageMMR": dht.int_, \
        "RadiantTeamName": dht.string, "RadiantTeamLogo": dht.string, "RadiantTeamID": dht.int_, "RadiantScore": dht.int_, "RadiantPlayerIDs": dht.int_array, \
        "DireTeamName": dht.string, "DireTeamLogo": dht.string, "DireTeamID": dht.int_, "DireScore": dht.int_, "DirePlayerIDs": dht.int_array, \
        "CurrentLeader": dht.string, "CurrentLead": dht.int_, "GameMode": dht.string, "BuildingState": dht.int_, \
        "PlayerNames": dht.string_array
    }
table_writer = DynamicTableWriter(live_match_col_defs)

live_dota2_matches = table_writer.table

def write_live_match_data():

    for i in range(num_pulls):

        start = time.time()

        resp = requests.get("https://api.opendota.com/api/live")

        if not resp.status_code == 200:
            print("The request for live matches was unsuccessful. Exiting...")
            sys.exit()

        live_match_data = json.loads(resp.content)

        for match in live_match_data:
            # Match ID, start time, end time, is active, league id, series id, average mmr
            match_id = int(match["match_id"])
            start_time = millis_to_datetime(match["activate_time"] * 1000)
            if match["deactivate_time"] == 0:
                end_time = now()
                is_active = True
            else:
                end_time = millis_to_datetime(match["deactivate_time"] * 1000)
                is_active = False
            league_id = match["league_id"]
            series_id = match["series_id"]
            average_mmr = match["average_mmr"]
            # Radiant team info
            radiant_team_name = match["team_name_radiant"]
            radiant_team_logo = match["team_logo_radiant"]
            radiant_team_id = match["team_id_radiant"]
            radiant_score = match["radiant_score"]
            radiant_player_ids = jpy.array("long", [item["account_id"] for item in match["players"][:5]])
            # Dire team info
            dire_team_name = match["team_name_dire"]
            dire_team_logo = match["team_logo_dire"]
            dire_team_id = match["team_id_dire"]
            dire_score = match["dire_score"]
            dire_player_ids = jpy.array("long", [item["account_id"] for item in match["players"][5:]])
            # Leader, lead, game mode, building state
            if match["radiant_lead"] > 0:
                leader = "radiant"
            elif match["radiant_lead"] < 0:
                leader = "dire"
            else:
                leader = "tied"
            lead = abs(match["radiant_lead"])
            game_mode = game_mode_from_id(match["game_mode"])
            building_state = match["building_state"]
            # Players, tags
            player_names = ["N/A"] * 10
            for idx, player in enumerate(match["players"]):
                if "name" in player.keys():
                    player_names[idx] = player["name"]
            player_names = jpy.array("java.lang.String", player_names)
        
            table_writer.write_row(\
                match_id, start_time, end_time, is_active, league_id, series_id, average_mmr, \
                radiant_team_name, radiant_team_logo, radiant_team_id, radiant_score, radiant_player_ids, \
                dire_team_name, dire_team_logo, dire_team_id, dire_score, dire_player_ids, \
                leader, lead, game_mode, building_state, \
                player_names
            )

        end = time.time()

        time.sleep(60 - (end - start))

live_match_data = live_dota2_matches.last_by(by=["MatchID"])

thread = threading.Thread(target=write_live_match_data)
thread.start()
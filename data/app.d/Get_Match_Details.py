# This script returns match data for a given match ID

def set_player_metric(obj, metric, key, keys):
    if key in keys:
        metric = obj[key]
    return metric

def set_detail_metric(obj, key, keys):
    if key in keys:
        return obj[key]
    return None

class D2P:
    def __init__(self, player_json):
        n_players = len(player_json)

        self.player_slots = [0] * n_players
        self.ability_targets = [{}] * n_players
        self.ability_upgrades = [[]] * n_players
        self.ability_uses = [{}] * n_players
        self.account_ids = [0] * n_players
        self.actions = [{}] * n_players
        self.additional_units = [0] * n_players
        self.assists = [0] * n_players
        self.backpacks = [[0, 0, 0, 0]] * n_players
        self.buyback_logs = [[{}]] * n_players
        self.camp_stacks = [0] * n_players
        self.connection_logs = [[]] * n_players
        self.creep_stacks = [0] * n_players
        self.damage = [{}] * n_players
        self.damage_inflictor = [{}] * n_players
        self.damage_inflictor_received = [{}] * n_players
        self.damage_taken = [{}] * n_players
        self.damage_targets = [{}] * n_players
        self.deaths = [0] * n_players
        self.denies = [0] * n_players
        self.dn_t = [[]] * n_players
        self.firstblood_claimed = [False] * n_players
        self.gold = [0] * n_players
        self.gold_per_min = [0] * n_players
        self.gold_reasons = [{}] * n_players
        self.gold_spent = [0] * n_players
        self.gold_t = [[]] * n_players
        self.hero_damage = [0] * n_players
        self.hero_healing = [0] * n_players
        self.hero_hits = [{}] * n_players
        self.hero_ids = [0] * n_players
        self.items = [[0, 0, 0, 0, 0, 0]] * n_players
        self.items_neutral = [0] * n_players
        self.item_uses = [{}] * n_players
        self.kill_streaks = [{}] * n_players
        self.killed = [{}] * n_players
        self.killed_by = [{}] * n_players
        self.kills = [0] * n_players
        self.kill_logs = [[{}]] * n_players
        self.lane_pos = [{}] * n_players
        self.last_hits = [0] * n_players
        self.leaver_statuses = [False] * n_players
        self.levels = [0] * n_players
        self.lh_t = [[]] * n_players
        self.life_states = [{}] * n_players
        self.max_hero_hits = [{}] * n_players
        self.multi_kills = [{}] * n_players
        self.net_worths = [0] * n_players
        self.observers = [{}] * n_players
        self.obs_left_logs = [[{}]] * n_players
        self.obs_logs = [[{}]] * n_players
        self.obs_placed = [0] * n_players
        self.party_ids = [0] * n_players
        self.party_sizes = [0] * n_players
        self.performance_others = [0] * n_players
        self.permanent_buffs = [[{}]] * n_players
        self.pings = [0] * n_players
        self.pred_victs = [False] * n_players
        self.purchases = [{}] * n_players
        self.purchase_logs = [[{}]] * n_players
        self.randoms = [False] * n_players
        self.repicks = [None] * n_players
        self.roshans_killed = [0] * n_players
        self.rune_pickups = [0] * n_players
        self.runes = [{}] * n_players
        self.rune_logs = [[{}]] * n_players
        self.sens = [{}] * n_players
        self.sen_left_logs = [[{}]] * n_players
        self.sen_logs = [[{}]] * n_players
        self.sen_places = [0] * n_players
        self.stuns = [0.] * n_players
        self.teamfight_participation = [0.] * n_players
        self.times = [[]] * n_players
        self.tower_damage = [0] * n_players
        self.towers_killed = [0] * n_players
        self.xp_per_min = [0] * n_players
        self.xp_reasons = [{}] * n_players
        self.xp_t = [[]] * n_players
        self.persona_names = [""] * n_players
        self.names = [""] * n_players
        self.last_logins = [""] * n_players
        self.gold_totals = [0] * n_players
        self.xp_totals = [0] * n_players
        self.kpms = [0.] * n_players
        self.kdas = [0] * n_players
        self.abandons = [0] * n_players
        self.neutral_kills = [0] * n_players
        self.tower_kills = [0] * n_players
        self.courier_kills = [0] * n_players
        self.lane_kills = [0] * n_players
        self.hero_kills = [0] * n_players
        self.obs_kills = [0] * n_players
        self.sentry_kills = [0] * n_players
        self.roshan_kills = [0] * n_players
        self.necronomicon_kills = [0] * n_players
        self.ancient_kills = [0] * n_players
        self.buyback_counts = [0] * n_players
        self.observer_uses = [0] * n_players
        self.sentry_uses = [0] * n_players
        self.lane_efficiencies = [0.] * n_players
        self.lane_efficiency_pcts = [0.] * n_players
        self.lanes = [0] * n_players
        self.lane_roles = [0] * n_players
        self.roamers = [False] * n_players
        self.purchase_times = [{}] * n_players
        self.first_purchase_times = [{}] * n_players
        self.item_wins = [{}] * n_players
        self.item_usages = [{}] * n_players
        self.ward_observer_purchases = [0] * n_players
        self.sentry_ward_purchases = [0] * n_players
        self.tpscroll_purchases = [0] * n_players
        self.gem_purchases = [0] * n_players
        self.apms = [0.] * n_players
        self.life_states_dead = [0] * n_players
        self.rank_tiers = [0] * n_players
        self.cosmetics = [[{}]] * n_players
        self.benchmarks = [{}] * n_players

        for idx in range(n_players):
            keys = list(player_json[idx].keys())
            self.player_slots[idx] = set_player_metric(player_json[idx], self.player_slots[idx], "player_slot", keys)
            self.ability_targets[idx] = set_player_metric(player_json[idx], self.ability_targets[idx], "ability_targets", keys)
            self.ability_upgrades[idx] = set_player_metric(player_json[idx], self.ability_upgrades[idx], "ability_upgrades_arr", keys)
            self.ability_uses[idx] = set_player_metric(player_json[idx], self.ability_uses[idx], "ability_uses", keys)
            self.account_ids[idx] = set_player_metric(player_json[idx], self.account_ids[idx], "account_id", keys)
            self.actions[idx] = set_player_metric(player_json[idx], self.actions[idx], "actions", keys)
            self.additional_units[idx] = set_player_metric(player_json[idx], self.additional_units[idx], "actions", keys)
            self.assists[idx] = set_player_metric(player_json[idx], self.assists[idx], "assists", keys)
            for bnum in range(4):
                self.backpacks[idx][bnum] = set_player_metric(player_json[idx], self.backpacks[idx][bnum], f"backpack_{bnum}", keys)
            self.buyback_logs[idx] = set_player_metric(player_json[idx], self.buyback_logs[idx], "buyback_log", keys)
            self.camp_stacks[idx] = set_player_metric(player_json[idx], self.camp_stacks[idx], "camps_stacked", keys)
            self.connection_logs[idx] = set_player_metric(player_json[idx], self.connection_logs[idx], "connection_log", keys)
            self.creep_stacks[idx] = set_player_metric(player_json[idx], self.creep_stacks[idx], "creeps_stacked", keys)
            self.damage[idx] = set_player_metric(player_json[idx], self.damage[idx], "damage", keys)
            self.damage_inflictor[idx] = set_player_metric(player_json[idx], self.damage_inflictor[idx], "damage_inflictor", keys)
            self.damage_inflictor_received[idx] = set_player_metric(player_json[idx], self.damage_inflictor_received[idx], "damage_inflictor_received", keys)
            self.damage_taken[idx] = set_player_metric(player_json[idx], self.damage_taken[idx], "damage_taken", keys)
            self.damage_targets[idx] = set_player_metric(player_json[idx], self.damage_targets[idx], "damage_targets", keys)
            self.deaths[idx] = set_player_metric(player_json[idx], self.deaths[idx], "deaths", keys)
            self.denies[idx] = set_player_metric(player_json[idx], self.denies[idx], "denies", keys)
            self.dn_t[idx] = set_player_metric(player_json[idx], self.dn_t[idx], "dn_t", keys)
            self.firstblood_claimed[idx] = set_player_metric(player_json[idx], self.firstblood_claimed[idx], "firstblood_claimed", keys)
            self.gold[idx] = set_player_metric(player_json[idx], self.gold[idx], "gold", keys)
            self.gold_per_min[idx] = set_player_metric(player_json[idx], self.gold_per_min[idx], "gold_per_min", keys)
            self.gold_reasons[idx] = set_player_metric(player_json[idx], self.gold_reasons[idx], "gold_reasons", keys)
            self.gold_spent[idx] = set_player_metric(player_json[idx], self.gold_spent[idx], "gold_spent", keys)
            self.gold_t[idx] = set_player_metric(player_json[idx], self.gold_t[idx], "gold_t", keys)
            self.hero_damage[idx] = set_player_metric(player_json[idx], self.hero_damage[idx], "hero_damage", keys)
            self.hero_healing[idx] = set_player_metric(player_json[idx], self.hero_healing[idx], "hero_healing", keys)
            self.hero_hits[idx] = set_player_metric(player_json[idx], self.hero_hits[idx], "hero_hits", keys)
            self.hero_ids[idx] = set_player_metric(player_json[idx], self.hero_ids[idx], "hero_id", keys)
            for inum in range(6):
                self.items[idx][inum] = set_player_metric(player_json[idx], self.items[idx][inum], f"item_{inum}", keys)
            self.items_neutral[idx] = set_player_metric(player_json[idx], self.items_neutral[idx], "item_neutral", keys)
            self.item_uses[idx] = set_player_metric(player_json[idx], self.item_uses[idx], "item_uses", keys)
            self.kill_streaks[idx] = set_player_metric(player_json[idx], self.kill_streaks[idx], "kill_streaks", keys)
            self.killed[idx] = set_player_metric(player_json[idx], self.killed[idx], "killed", keys)
            self.killed_by[idx] = set_player_metric(player_json[idx], self.killed_by[idx], "killed_by", keys)
            self.kills[idx] = set_player_metric(player_json[idx], self.kills[idx], "kills", keys)
            self.kill_logs[idx] = set_player_metric(player_json[idx], self.kill_logs[idx], "kills_log", keys)
            self.lane_pos[idx] = set_player_metric(player_json[idx], self.lane_pos[idx], "lane_pos", keys)
            self.last_hits[idx] = set_player_metric(player_json[idx], self.last_hits[idx], "last_hits", keys)
            self.leaver_statuses[idx] = set_player_metric(player_json[idx], self.leaver_statuses[idx], "leaver_status", keys)
            self.levels[idx] = set_player_metric(player_json[idx], self.levels[idx], "level", keys)
            self.lh_t[idx] = set_player_metric(player_json[idx], self.lh_t[idx], "lh_t", keys)
            self.life_states[idx] = set_player_metric(player_json[idx], self.life_states[idx], "life_state", keys)
            self.max_hero_hits[idx] = set_player_metric(player_json[idx], self.max_hero_hits[idx], "max_hero_hit", keys)
            self.multi_kills[idx] = set_player_metric(player_json[idx], self.multi_kills[idx], "multi_kills", keys)
            self.net_worths[idx] = set_player_metric(player_json[idx], self.net_worths[idx], "net_worth", keys)
            self.observers[idx] = set_player_metric(player_json[idx], self.observers[idx], "obs", keys)
            self.obs_left_logs[idx] = set_player_metric(player_json[idx], self.obs_left_logs[idx], "obs_left_log", keys)
            self.obs_logs[idx] = set_player_metric(player_json[idx], self.obs_logs[idx], "obs_log", keys)
            self.obs_placed[idx] = set_player_metric(player_json[idx], self.obs_placed[idx], "obs_placed", keys)
            self.party_ids[idx] = set_player_metric(player_json[idx], self.party_ids[idx], "party_id", keys)
            self.party_sizes[idx] = set_player_metric(player_json[idx], self.party_sizes[idx], "party_size", keys)
            self.performance_others[idx] = set_player_metric(player_json[idx], self.performance_others[idx], "performance_others", keys)
            self.permanent_buffs[idx] = set_player_metric(player_json[idx], self.permanent_buffs[idx], "permanent_buffs", keys)
            self.pings[idx] = set_player_metric(player_json[idx], self.pings[idx], "pings", keys)
            self.pred_victs[idx] = set_player_metric(player_json[idx], self.pred_victs[idx], "pred_vict", keys)
            self.purchases[idx] = set_player_metric(player_json[idx], self.purchases[idx], "purchase", keys)
            self.purchase_logs[idx] = set_player_metric(player_json[idx], self.purchase_logs[idx], "purchase_log", keys)
            self.randoms[idx] = set_player_metric(player_json[idx], self.randoms[idx], "randomed", keys)
            self.repicks[idx] = set_player_metric(player_json[idx], self.repicks[idx], "repicked", keys)
            self.roshans_killed[idx] = set_player_metric(player_json[idx], self.roshans_killed[idx], "roshans_killed", keys)
            self.rune_pickups[idx] = set_player_metric(player_json[idx], self.rune_pickups[idx], "rune_pickups", keys)
            self.runes[idx] = set_player_metric(player_json[idx], self.runes[idx], "runes", keys)
            self.rune_logs[idx] = set_player_metric(player_json[idx], self.rune_logs[idx], "runes_log", keys)
            self.sens[idx] = set_player_metric(player_json[idx], self.sens[idx], "sen", keys)
            self.sen_left_logs[idx] = set_player_metric(player_json[idx], self.sen_left_logs[idx], "sen_left_log", keys)
            self.sen_logs[idx] = set_player_metric(player_json[idx], self.sen_logs[idx], "sen_log", keys)
            self.sen_places[idx] = set_player_metric(player_json[idx], self.sen_places[idx], "sen_placed", keys)
            self.stuns[idx] = set_player_metric(player_json[idx], self.stuns[idx], "stuns", keys)
            self.teamfight_participation[idx] = set_player_metric(player_json[idx], self.teamfight_participation[idx], "teamfight_participation", keys)
            self.times[idx] = set_player_metric(player_json[idx], self.times[idx], "times", keys)
            self.tower_damage[idx] = set_player_metric(player_json[idx], self.tower_damage[idx], "tower_damage", keys)
            self.towers_killed[idx] = set_player_metric(player_json[idx], self.towers_killed[idx], "towers_killed", keys)
            self.xp_per_min[idx] = set_player_metric(player_json[idx], self.xp_per_min[idx], "xp_per_min", keys)
            self.xp_reasons[idx] = set_player_metric(player_json[idx], self.xp_reasons[idx], "xp_reasons", keys)
            self.xp_t[idx] = set_player_metric(player_json[idx], self.xp_t[idx], "xp_t", keys)
            self.persona_names[idx] = set_player_metric(player_json[idx], self.persona_names[idx], "personaname", keys)
            self.names[idx] = set_player_metric(player_json[idx], self.names[idx], "name", keys)
            self.last_logins[idx] = set_player_metric(player_json[idx], self.last_logins[idx], "last_login", keys)
            self.gold_totals[idx] = set_player_metric(player_json[idx], self.gold_totals[idx], "total_gold", keys)
            self.xp_totals[idx] = set_player_metric(player_json[idx], self.xp_totals[idx], "total_xp", keys)
            self.kpms[idx] = set_player_metric(player_json[idx], self.kpms[idx], "kills_per_min", keys)
            self.kdas[idx] = set_player_metric(player_json[idx], self.kdas[idx], "kda", keys)
            self.abandons[idx] = set_player_metric(player_json[idx], self.abandons[idx], "abandons", keys)
            self.neutral_kills[idx] = set_player_metric(player_json[idx], self.neutral_kills[idx], "neutral_kills", keys)
            self.tower_kills[idx] = set_player_metric(player_json[idx], self.tower_kills[idx], "tower_kills", keys)
            self.courier_kills[idx] = set_player_metric(player_json[idx], self.courier_kills[idx], "courier_kills", keys)
            self.lane_kills[idx] = set_player_metric(player_json[idx], self.lane_kills[idx], "lane_kills", keys)
            self.hero_kills[idx] = set_player_metric(player_json[idx], self.hero_kills[idx], "hero_kills", keys)
            self.obs_kills[idx] = set_player_metric(player_json[idx], self.obs_kills[idx], "observer_kills", keys)
            self.sentry_kills[idx] = set_player_metric(player_json[idx], self.sentry_kills[idx], "sentry_kills", keys)
            self.roshan_kills[idx] = set_player_metric(player_json[idx], self.roshan_kills[idx], "roshan_kills", keys)
            self.necronomicon_kills[idx] = set_player_metric(player_json[idx], self.necronomicon_kills[idx], "necronomicon_kills", keys)
            self.ancient_kills[idx] = set_player_metric(player_json[idx], self.ancient_kills[idx], "ancient_kills", keys)
            self.buyback_counts[idx] = set_player_metric(player_json[idx], self.buyback_counts[idx], "buyback_count", keys)
            self.observer_uses[idx] = set_player_metric(player_json[idx], self.observer_uses[idx], "observer_uses", keys)
            self.sentry_uses[idx] = set_player_metric(player_json[idx], self.sentry_uses[idx], "sentry_uses", keys)
            self.lane_efficiencies[idx] = set_player_metric(player_json[idx], self.lane_efficiencies[idx], "lane_efficiency", keys)
            self.lane_efficiency_pcts[idx] = set_player_metric(player_json[idx], self.lane_efficiency_pcts[idx], "lane_efficiency_pct", keys)
            self.lanes[idx] = set_player_metric(player_json[idx], self.lanes[idx], "lane", keys)
            self.lane_roles[idx] = set_player_metric(player_json[idx], self.lane_roles[idx], "lane_role", keys)
            self.roamers[idx] = set_player_metric(player_json[idx], self.roamers[idx], "is_roaming", keys)
            self.purchase_times[idx] = set_player_metric(player_json[idx], self.purchase_times[idx], "purchase_time", keys)
            self.first_purchase_times[idx] = set_player_metric(player_json[idx], self.first_purchase_times[idx], "first_purchase_time", keys)
            self.item_wins[idx] = set_player_metric(player_json[idx], self.item_wins[idx], "item_win", keys)
            self.item_usages[idx] = set_player_metric(player_json[idx], self.item_usages[idx], "item_usage", keys)
            self.ward_observer_purchases[idx] = set_player_metric(player_json[idx], self.ward_observer_purchases[idx], "purchase_ward_observer", keys)
            self.sentry_ward_purchases[idx] = set_player_metric(player_json[idx], self.sentry_ward_purchases[idx], "purchase_ward_sentry", keys)
            self.tpscroll_purchases[idx] = set_player_metric(player_json[idx], self.tpscroll_purchases[idx], "purchase_tpscroll", keys)
            self.gem_purchases[idx] = set_player_metric(player_json[idx], self.gem_purchases[idx], "purchase_gem", keys)
            self.apms[idx] = set_player_metric(player_json[idx], self.apms[idx], "actions_per_min", keys)
            self.life_states_dead[idx] = set_player_metric(player_json[idx], self.life_states_dead[idx], "life_state_dead", keys)
            self.rank_tiers[idx] = set_player_metric(player_json[idx], self.rank_tiers[idx], "rank_tier", keys)
            self.cosmetics[idx] = set_player_metric(player_json[idx], self.cosmetics[idx], "cosmetics", keys)
            self.benchmarks[idx] = set_player_metric(player_json[idx], self.benchmarks[idx], "benchmarks", keys)

class D2D:
    def __init__(self, match_json):
        keys = list(match_json.keys())
        self.barracks_status_dire = set_detail_metric(match_json, "barracks_status_dire", keys)
        self.barracks_status_radiant = set_detail_metric(match_json, "barracks_status_radiant", keys)
        self.cluster = set_detail_metric(match_json, "cluster", keys)
        self.dire_score = set_detail_metric(match_json, "dire_score", keys)
        self.dire_team_id = set_detail_metric(match_json, "dire_team_id", keys)
        self.duration = set_detail_metric(match_json, "duration", keys)
        self.engine = set_detail_metric(match_json, "engine", keys)
        self.first_blood_time = set_detail_metric(match_json, "first_blood_time", keys)
        self.game_mode = set_detail_metric(match_json, "game_mode", keys)
        self.league_id = set_detail_metric(match_json, "league_id", keys)
        self.lobby_type = set_detail_metric(match_json, "lobby_type", keys)
        self.match_seq_num = set_detail_metric(match_json, "match_seq_num", keys)
        self.negative_votes = set_detail_metric(match_json, "negative_votes", keys)
        self.objectives = set_detail_metric(match_json, "objectives", keys)
        self.positive_votes = set_detail_metric(match_json, "positive_votes", keys)
        self.radiant_gold_adv = set_detail_metric(match_json, "radiant_gold_adv", keys)
        self.radiant_score = set_detail_metric(match_json, "radiant_score", keys)
        self.radiant_team_id = set_detail_metric(match_json, "radiant_team_id", keys)
        self.radiant_win = set_detail_metric(match_json, "radiant_win", keys)
        self.radiant_xp_adv = set_detail_metric(match_json, "radiant_xp_adv", keys)
        self.skill = set_detail_metric(match_json, "skill", keys)
        self.start_time = set_detail_metric(match_json, "start_time", keys)
        self.tower_status_dire = set_detail_metric(match_json, "tower_status_dire", keys)
        self.tower_status_radiant = set_detail_metric(match_json, "tower_status_radiant", keys)
        self.version = set_detail_metric(match_json, "version", keys)
        self.replay_salt = set_detail_metric(match_json, "replay_salt", keys)
        self.series_id = set_detail_metric(match_json, "series_id", keys)
        self.series_type = set_detail_metric(match_json, "series_type", keys)
        self.league = set_detail_metric(match_json, "league", keys)
        self.radiant_team = set_detail_metric(match_json, "radiant_team", keys)
        self.dire_team = set_detail_metric(match_json, "dire_team", keys)
        self.patch = set_detail_metric(match_json, "patch", keys)
        self.region = set_detail_metric(match_json, "region", keys)
        self.throw = set_detail_metric(match_json, "throw", keys)
        self.loss = set_detail_metric(match_json, "loss", keys)
        self.replay_url = set_detail_metric(match_json, "replay_url", keys)

class D2M:
    def __init__(self, id):
        self.id = id
        self.Details = None
        self.Players = None
        self.teamfights = None
        self.chat = None
        self.draft = None

def get_dota2_match(match_id):

    resp = requests.get(f"https://api.opendota.com/api/matches/{match_id}")

    if not(resp.status_code == 200):
        print(f"Response code {resp.status_code}. The request for match ID {match_id} failed.")
        return None

    match_json = resp.json()

    Match = D2M(match_json["match_id"])
    # Match = D2M(match_id)

    # Players
    Match.Players = D2P(match_json["players"])
    # Draft
    draft = []
    if match_json["draft_timings"]:
        for pick_ban in match_json["draft_timings"]:
            hero_name = Dota2.Heroes.dataframe.loc[Dota2.Heroes.dataframe["id"] == pick_ban["hero_id"], "LocalizedName"].iloc[0]
            if not(pick_ban["player_slot"]):
                pick_ban["player_slot"] = -1
            draft.append({\
                "IsPick": pick_ban["pick"], \
                "Hero": hero_name, \
                "PlayerSlot": pick_ban["player_slot"], \
                "ExtraTime": pick_ban["extra_time"], \
                "TimeTaken": pick_ban["total_time_taken"]\
            })
        Match.draft = dhp.to_table(pd.DataFrame(draft))\
            .update(["IsPick = (boolean)IsPick", "Hero = (java.lang.String)Hero", \
                "PlayerSlot = (short)PlayerSlot", "ExtraTime = (short)ExtraTime", "TimeTaken = (short)TimeTaken"])
    else:
        Match.draft = None
    # Chat
    chat = []
    if match_json["chat"]:
        for chat_item in match_json["chat"]:
            chat.append({"Time": chat_item["time"], "Contents": chat_item["key"], "PlayerNum": chat_item["slot"]})
        Match.chat = dhp.to_table(pd.DataFrame(chat))\
            .update(["Time = (int)Time", "Contents = (java.lang.String)Contents", "PlayerNum = (byte)PlayerNum"])
    else:
        Match.chat = None
    # Team fights
    Match.teamfights = match_json["teamfights"]
    # Details
    Match.Details = D2D(match_json)

    return Match

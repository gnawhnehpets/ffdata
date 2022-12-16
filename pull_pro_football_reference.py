import requests 
from bs4 import BeautifulSoup
import pymongo
import pandas as pd
from dateutil import parser
import time 
import datetime
import json
import random
# from tqdm import tqdm
from progress.bar import Bar
# import numpy as np

class BaseApi():
	def _call(self, url):
		result_json_string = requests.get(url);
		try:
			result_json_string.raise_for_status()
		except requests.exceptions.HTTPError as e:
			return e
			#return SleeperWrapperException("Empty value returned")
		result = result_json_string.json()
		return result

class Players(BaseApi):
	def __init__(self):
		pass

	def get_all_players(self):
		return self._call("https://api.sleeper.app/v1/players/nfl")

	def get_trending_players(self,sport, add_drop, hours=24, limit=25 ):
		return self._call("https://api.sleeper.app/v1/players/{}/trending/{}?lookback_hours={}&limit={}".format(sport, add_drop, hours, limit))


client = pymongo.MongoClient("mongodb+srv://stephen:password!@sandbox.vmm0n.mongodb.net/?retryWrites=true&w=majority")

db = client['ffdata']
db.playerdata.drop()
db.create_collection('playerdata')

# response = requests.get("https://api.sleeper.app/v1/players/nfl")
players = Players() 
all_players = players.get_all_players() # get all players from sleeper API
# db.leaguedata.insert_many([all_players])
total_count = len(all_players)
count = 0
bar = Bar('Processing', max=total_count)

key, val = random.choice(list(all_players.items()))
print(key, val)

for id, player in all_players.items():
    # print(player['player_id'])
	print(player)
	if player['position'] != 'DEF':
		doc = {
				"ids":{
					"player_id": player["player_id"], 
					"stats_id": player["stats_id"], 
					"pandascore_id": player["pandascore_id"], 
					"gsis_id": player["gsis_id"], 
					"swish_id": player["swish_id"], 
					"sportradar_id": player["sportradar_id"], 
					"yahoo_id": player["yahoo_id"], 
					"rotowire_id": player["rotowire_id"], 
					"espn_id": player["espn_id"], 
					"fantasy_data_id": player["fantasy_data_id"], 
					"rotoworld_id": player["rotoworld_id"], 
				}, 
				"injuries":{
					"injury_body_part": player["injury_body_part"], 
					"injury_start_date": player["injury_start_date"], 
					"injury_status": player["injury_status"], 
					"injury_notes": player["injury_notes"], 
					"practice_description": player["practice_description"], 
					"practice_participation": player["practice_participation"], 
					"news_updated": player["news_updated"], 
				}, 
				"player": {
					"full_name": player["full_name"], 
					"first_name": player["first_name"], 
					"last_name": player["last_name"], 
					"search_full_name": player["search_full_name"], 
					"search_first_name": player["search_first_name"], 
					"search_last_name": player["search_last_name"], 
					"birth_date": player["birth_date"], 
					"age": player["age"], 
					"height": player["height"], 
					"weight": player["weight"], 
					"team": player["team"], 
					"status": player["status"], 
					"active": player["active"], 
					"position": player["position"], 
					"fantasy_positions": player["fantasy_positions"], 
					"depth_chart_order": player["depth_chart_order"], 
					"depth_chart_position": player["depth_chart_position"], 
				}, 
				"misc": {
					"number": player["number"], 
					"high_school": player["high_school"], 
					"search_rank": player["search_rank"], 
					"years_exp": player["years_exp"], 
					"hashtag": player["hashtag"], 
					"college": player["college"], 
					"birth_country": player["birth_country"], 
					"metadata": player["metadata"], 
					"sport": player["sport"], 
					"birth_city": player["birth_city"], 
					"birth_state": player["birth_state"], 
				} 
			}
		db.playerdata.insert_one(doc)
		bar.next()
	else:
		pass
# for x in all_players[0:5]:
# 	# print(x, all_players[x])
# 	db.playerdata.insert_one(all_players[x]); 
# 	bar.next()
# print(all_players[1])
bar.finish()
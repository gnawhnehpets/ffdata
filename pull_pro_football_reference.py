import requests 
from bs4 import BeautifulSoup
import pymongo
import pandas as pd
from dateutil import parser
import time 
import datetime
import json
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
# print(response)
players = Players()
all_players = players.get_all_players()
# db.leaguedata.insert_many([all_players])
total_count = len(all_players)
count = 0
for x in all_players:
    count+=1
    if count % 100 == 0: print(str(count*100/total_count) + "%")
    # print(x, all_players[x])
    db.playerdata.insert_one(all_players[x])
# print(all_players[1])
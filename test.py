from riotwatcher import RiotWatcher
import config
import util

# watcher = RiotWatcher(config.api_key)
# profile = watcher.summoner.by_name(config.my_region,config.playerName)
# result = watcher.match.matchlist_by_account(
#     config.my_region,
#     profile['accountId'],
#     (420)
#     ,end_time=1567818270906
#     )
# util.saveJSON("lastX.json",result)

# arr = [ 1 ,2 ,3 ,4]
# top10 = arr[0:10]
# print(top10)

from keras.models import load_model
import pandas as pd
import os

# model = load_model("Lingering.h5")
# df = pd.read_csv(os.path.join("analysis","dudehacker","data_scaled.csv"))
# result = model.evaluate(df.drop('win',axis=1), df[['win']], verbose=0)
# print(result)

# model = load_model("dudehacker.h5")
# df = pd.read_csv(os.path.join("analysis","Lingering","data_scaled.csv"))
# result = model.evaluate(df.drop('win',axis=1), df[['win']], verbose=0)
# print(result)

# from prepData import DataPrep
folder = os.path.join("analysis","all")
# prep = DataPrep(folder)
# prep.split()

from analysis import Analysis
a = Analysis(folder)
a.build()
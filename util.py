import jsonpickle
import json
import urllib.request
import config
import os
from pathlib import Path
from datetime import datetime
import csv

aWeekInMs=1000*60*60*24*7

def listToCsv(filename,listOfObjects):
    if listOfObjects:
        # print(listOfObjects)
        path = Path(filename)
        os.makedirs(path.parent,exist_ok=True)
        with open(filename,'w+',newline='') as csvFile:
            keys = listOfObjects[0].keys()
            writer = csv.DictWriter(csvFile,fieldnames=keys)
            writer.writeheader()
            writer.writerows(listOfObjects)
        print(f"{filename} is saved")
    else:
        print("invalid list",listOfObjects)

def toDate(timestamp):
    date = datetime.utcfromtimestamp(timestamp//1000)
    print(date)

def readJSON(filename):
    with open(filename) as jsonFile:
        data = json.load(jsonFile)
        return data

def saveJSON(filename="data.json", data="no data", subfolder="templates"):
    # print(data)
    print(f"file {filename} saved")
    jsonString = jsonpickle.encode(data)
    prettyJson = json.dumps(json.loads(jsonString), indent=4, sort_keys=True)
    folder = config.dataDir + "\\" + subfolder 
    os.makedirs(folder,exist_ok=True)
    f = open(folder + "\\" + filename, "w+")
    f.write(prettyJson)
    f.close()


def getJsonFromUrl(url):
    with urllib.request.urlopen(url) as url2:
        data = json.loads(url2.read().decode())
        return data
from urllib.parse import urlunparse
import config
import util

# champion info
# s = "http://ddragon.leagueoflegends.com/cdn/9.20.1/data/en_US/champion.json"


def getCurrentPatch():
    # patchByRegion = "https://ddragon.leagueoflegends.com/realms/na.json"
    currentPatch = "https://ddragon.leagueoflegends.com/api/versions.json"
    patchInfo = util.getJsonFromUrl(currentPatch)
    return patchInfo[0]

# getCurrentPatch()


def getChampionUrl():
    scheme = "http"
    netloc = "ddragon.leagueoflegends.com"
    path = "/cdn/"+getCurrentPatch()+"/data/"+config.locale+"/champion.json"
    url = urlunparse((scheme, netloc, path, '', '', ''))
    return url


def updateChampions():
    champions = util.getJsonFromUrl(getChampionUrl())
    util.saveJSON("champions.json", champions)

def getChampionId(championName):
    template = "data\\templates\\champions.json"
    champions = util.readJSON(template)
    data = champions['data']
    # print(data)
    for key in data.keys():
        if data[key]['name'] == championName:
            return data[key]['key']

    raise Exception(f"{championName} is not found")
 


def getChampionName(championId):
    template = "data\\templates\\champions.json"
    champions = util.readJSON(template)
    data = champions['data']
    # print(data)
    for key in data.keys():
        if data[key]['key'] == str(championId):
            return data[key]['name']

    print(f"{championId} is not found, need update {template}")
    updateChampions()
 

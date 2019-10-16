from riotwatcher import RiotWatcher, ApiError
import util
import config
import ddragon
import os
from datetime import datetime, timedelta

watcher = RiotWatcher(config.api_key)

# get last 100 ranked matches to use as train and test dataset


def getPreviousWeekGames(encryptedAccount, gameCreationTime):
    end = gameCreationTime
    result = watcher.match.matchlist_by_account(
        config.my_region,
        encryptedAccount,
        (420),
        begin_time=end-util.aWeekInMs,
        end_time=end
    )
    return result

def parsePreviousGames(encryptedAccount,gameCreationTime):
    pastGames = getPreviousWeekGames(encryptedAccount,gameCreationTime)
    # util.saveJSON(f"{gameCreationTime}_{encryptedAccount}_history.json",pastGames)
    output = {}
    wins = 0
    maxLoseStreak = 0
    loseStreak = 0
    for game in pastGames['matches']:
        try: 
            gameDetails = watcher.match.by_id(config.my_region,game['gameId'])
            for i in range(0, 10):
                playerMetadata = gameDetails['participantIdentities'][i]
                playerData = gameDetails['participants'][i]
                playerName = playerMetadata['player']['currentAccountId']
                if playerName == encryptedAccount:
                    if playerData['stats']['win']: 
                        wins = wins + 1
                        loseStreak = 0
                    else:
                        loseStreak = loseStreak + 1
                        if maxLoseStreak < loseStreak:
                            maxLoseStreak = loseStreak
                    break
        except ApiError as err:
            if err.response.status_code == 429:
                # print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
                print('this retry-after is handled by default by the RiotWatcher library')
                print('future requests wait until the retry-after time passes')
            else:
                raise
    output['winRate'] = wins / len(pastGames['matches'])
    output['maxLoseStreak'] = maxLoseStreak
    print(output)
    return output

def downloadLastestMatches():
    matches = watcher.match.matchlist_by_account(
        config.my_region, me['accountId'], queue=(420))
    util.saveJSON("matches.json", matches, config.playerName)

    # each match detail
    matchList = matches['matches']
    for match in matchList:
        game = watcher.match.by_id(config.my_region, match['gameId'])
        util.saveJSON(
            "match_"+str(match['gameId'])+".json", game, config.playerName)
    print("downloaded latest 100 matches")


def parseMatch(filename):
    team = None
    now = datetime.now()
    data = util.readJSON(filename)
    print("parsing ", filename)
    output = {}
    output['gameId'] = data['gameId']
    # check if already parsed
    outputFile = f"data\\{config.playerName}\\data_{data['gameId']}.json"
    if os.path.exists(outputFile): 
        return util.readJSON(outputFile)
    
    # start parsing
    for i in range(0, 10):
        playerMetadata = data['participantIdentities'][i]
        playerData = data['participants'][i]
        playerName = playerMetadata['player']['summonerName']
        if playerName == config.playerName:
            output['win'] = playerData['stats']['win']
            team = playerData['teamId']

    for i in range(0, 10):
        playerMetadata = data['participantIdentities'][i]
        playerData = data['participants'][i]
        championId = playerData['championId']
        prefix = ''
        # gather teammates data
        if playerData['teamId'] == team:
            if i > 4:
                prefix = 'teammate'+str(i - 5) + '_'
            else:
                prefix = 'teammate' + str(i) + '_'

            summonerId = playerMetadata['player']['summonerId']
            championData = watcher.champion_mastery.by_summoner_by_champion(
                config.my_region, summonerId, championId)
            output[prefix+'championPoints'] = championData['championPoints']
            secondsSinceLastPlayed = int(datetime.timestamp(
                now)) - championData['lastPlayTime']//1000
            td = timedelta(seconds=secondsSinceLastPlayed)
            output[prefix+'championDaysSinceLastPlayed'] = td.days
            playerHistory = parsePreviousGames(playerMetadata['player']['currentAccountId'],data['gameCreation'])
            output[prefix+'playerPastWeekWinRate']=playerHistory['winRate']
            output[prefix+'playerPastWeekLoseStreak']=playerHistory['maxLoseStreak']
        else:
            if i > 4:
                prefix = 'enemy'+str(i - 5) + '_'
            else:
                prefix = 'enemy' + str(i) + '_'

        # championName = ddragon.getChampionName(championId)
        output[prefix+"champion"] = championId
    print(f"Win: {output['win']}")
    util.saveJSON(outputFile,output,config.playerName)
    return output


def createDerivedInputCsv():
    folder = "data\\"+config.playerName
    if os.path.exists(folder) & os.path.isdir(folder):
        # parse each match
        print(f"parsing matches in folder {folder}")
        matchList = []
        for f in os.listdir(folder):
            if f.startswith("match_"):
                # print(f)
                row = parseMatch(folder+"\\"+f)
                matchList.append(row)

        util.listToCsv("data.csv", matchList)

    else:
        print(f"{folder} does not exist")


# profile
me = watcher.summoner.by_name(config.my_region, config.playerName)
util.saveJSON("profile.json", me, config.playerName)

# downloadLastestMatches()

createDerivedInputCsv()

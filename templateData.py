from riotwatcher import RiotWatcher, ApiError
import util
import config
import ddragon

watcher = RiotWatcher(config.api_key)

# champions
ddragon.updateChampions()

# profile
me = watcher.summoner.by_name(config.my_region, config.playerName)
util.saveJSON("profile.json", me)

# ranked stats
my_ranked_stats = watcher.league.by_summoner(config.my_region, me['id'])
util.saveJSON("ranked_stats.json", my_ranked_stats)

# matches
matches = watcher.match.matchlist_by_account(config.my_region, me['accountId'])
util.saveJSON("matches.json", matches)

# match detail
game = watcher.match.by_id(config.my_region,3147892203)
util.saveJSON("game.json",game)

# champion mastery
champion_mastery = watcher.champion_mastery.by_summoner_by_champion(config.my_region,me['id'],89)
util.saveJSON("champion_mastery.json",champion_mastery)
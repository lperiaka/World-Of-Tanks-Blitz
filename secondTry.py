import wargaming
from datetime import datetime, timedelta
#I use pretty print to print dictionary nicely since returned data is in json structure
import pprint

#My account ID is 1012192478

wotb = wargaming.WoTB('demo', language='en', region='na', enable_parser=True)
#Wargaming .NET
wgn = wargaming.WGN('demo', language='en', region='na')
clan = wotb.clans.list(search='2BOOM')[0]
#print(clan)
clan_id = str(clan['clan_id'])
clan_info = wotb.clans.info(clan_id=clan['clan_id'])[clan_id]
#print(clan_info)
members_ids = clan_info['members_ids']
#print(members_ids)
accounts = wotb.account.info(account_id=members_ids)
#accounts=dict(accounts)
#pprint.pprint(accounts)

#Prints my stats
maxBattles=0
for ID in members_ids:
    account=accounts[ID]
    battlesCount=account['statistics']['all']['battles']
    if battlesCount > maxBattles:
        maxBattles=battlesCount
    if account['nickname']=='sunnydog':
        #pprint.pprint(dict(account))
        pass
print()
#print('Max Battles: ' , maxBattles)
print()
myAchievments = wotb.account.achievements(account_id='1012192478')
#pprint.pprint(dict(myAchievments))
print()
allTanks=wotb.encyclopedia.vehicles()
tanksAndIds={}
#Finds names for all the tank IDs
for tank_id in allTanks:
    name=allTanks[tank_id]['name']
    tanksAndIds[name]=tank_id
#pprint.pprint(tanksAndIds)

#pprint.pprint(dict(allTanks))
tankStats=wotb.tanks.stats(account_id='1012192478',in_garage='1',access_token='',tank_id=tanksAndIds['SU-152'])
pprint.pprint(dict(tankStats))
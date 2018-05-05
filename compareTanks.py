import wargaming
import pprint
import time
import os
import pickle
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np

myID='1012192478'
allTankIDs=[]
tankInfo={}
wotb = wargaming.WoTB('demo', language='en', region='na', enable_parser=True)

def getVehicleInfo():
    # tankInfo is dictionary. Key is tank id and defnition is dict with keys 'name','nation', 'tier', 'type'
    global tankInfo
    tankInfo=wotb.encyclopedia.vehicles(fields=['name','nation','tier','type'])
    for tankID in tankInfo:
        allTankIDs.append(tankID)
    #pprint.pprint(dict(tankInfo))

def compareStatistics(statToCompare,tierToCompare,typeToCompare):
    #Results is a dictionary with the country as the key and the value is a list of the selected stat for each tank for that country matching the restrictions
    results={}
    my_path = os.path.abspath('.\\tankData')
    for tankID in tankInfo:
        nation=str(tankInfo[tankID]['nation'])
        tier=str(tankInfo[tankID]['tier'])
        type=str(tankInfo[tankID]['type'])
        name=str(tankInfo[tankID]['name'])
        #print(tier, type)
        #print(type(tier))
        if(tier==tierToCompare and type==typeToCompare):
            #Each pickled file contains information about each tank. Name of file is the Tank ID
            #Need to do this to avoid exceeding API request limit
            path = my_path + "\\" + str(tankID)
            VehicleStats = pickle.load(open(path,"rb"))
            #pprint.pprint(VehicleStats)
            #print("VehicleStats[tankID]"+statToCompare)
            stat=eval("VehicleStats[tankID]"+statToCompare)
            #If tank with matching nation already in results dictionary, append stat to list for that country
            if nation in results:
                results[nation].append(stat)
            #If not, add new key into results dictionary
            else:
                results[nation]=[stat]

            print(str(stat) + ' ' + name + ' ' + nation)
    print(results)
    createHistogram(results, statToCompare)

def createHistogram(results,statToCompare):
    for country in results:
        results[country]=mean(results[country])
    print(results.keys())
    print(results.values())
    y_pos = np.arange(len(list(results.keys())))
    plt.bar(y_pos,results.values())
    plt.xticks(y_pos, list(results.keys()))
    plt.ylabel(statToCompare)
    plt.show()

def main():
    getVehicleInfo()
    #Vehicle Types: mediumTank, AT-SPG, lightTank, heavyTank
    #Nations: germany, usa, china, uk, other, france, ussr, japan
    #statToCompare should be in format '[index1][index2][index3]'
    #See https://developers.wargaming.net/reference/all/wotb/encyclopedia/vehicleprofile/?application_id=demo&tank_id=14145&r_realm=na&run=1 for formating of JSON file
    statToCompare="['gun']['aim_time']"
    tierToCompare='5'
    typeToCompare='heavyTank'
    compareStatistics(statToCompare,tierToCompare,typeToCompare)

if __name__ == "__main__":
    main()

'''clan = wotb.clans.list(search='2BOOM')[0]
accounts=wotb.account.info(account_id=myID,fields='nickname')
#accounts=accounts['1012192478']['statistics']
print(accounts['1012192478']['nickname'])'''
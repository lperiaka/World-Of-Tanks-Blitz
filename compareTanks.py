import wargaming
import pprint
import time
import os
import pickle
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import csv

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
        nation=str(tankInfo[tankID]['nation'])
        name=tankInfo[tankID]['name']
    #pprint.pprint(dict(tankInfo))

def compareStatistics(statToCompare,tierToCompare,typeToCompare, showPlot=False):
    #Results is a dictionary with the country as the key and the value is a list of the selected stat for each tank for that country matching the restrictions
    results={}
    my_path = os.path.abspath('.\\tankData')
    for tankID in tankInfo:
        #Need to convert to string so comparisons work properly
        nation=str(tankInfo[tankID]['nation'])
        tier=str(tankInfo[tankID]['tier'])
        type=str(tankInfo[tankID]['type'])
        name=str(tankInfo[tankID]['name'])
        if(tier==tierToCompare and type==typeToCompare):
            #Each pickled file contains information about each tank. Name of file is the Tank ID
            #Need to do this to avoid exceeding API request limit
            path = my_path + "\\" + str(tankID)
            VehicleStats = pickle.load(open(path,"rb"))
            #pprint.pprint(VehicleStats)
            #print("VehicleStats[tankID]"+statToCompare)
            #Extract the correct stat from the VehicalStats dictionary of dictionaris
            stat=eval("VehicleStats[tankID]"+statToCompare)
            #If tank with matching nation already in results dictionary, append stat to list for that country
            if nation in results:
                results[nation].append(stat)
            #If not, add new key into results dictionary
            else:
                results[nation]=[stat]

            #print(str(stat) + ' ' + name + ' ' + nation)
    for country in results:
        results[country]=mean(results[country])
    if(showPlot):
        createHistogram(results, statToCompare)
    return results

def createHistogram(results,ylabel):
    y_pos = np.arange(len(list(results.keys())))
    plt.bar(y_pos,results.values())
    plt.xticks(y_pos, list(results.keys()))
    plt.ylabel(ylabel)
    plt.show()

def compareNations():
    statsToCompare=[]
    finalScores={'germany':[], 'usa':[], 'china':[], 'uk':[], 'other':[], 'france':[], 'ussr':[], 'japan':[]}
    finalAvgScores={'germany': 0, 'usa': 0, 'china': 0, 'uk': 0, 'other': 0, 'france': 0, 'ussr': 0, 'japan': 0}
    with open('StatsToCompare.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        csvfile.readline()  # Read first line which is just header info
        for row in readCSV:
            statsToCompare.append([row[0],row[1]])
    #Iterate through each stat. The returned result contains average z score for all tiers and tank types for each nation
    #avgZScore={usa : 1.02, ussr...
    for item in statsToCompare:
        avgZScore=compareStatisticsAllTanks(item[0])
        if item[1]=='Low':#Need to flip z scores if a low score is actuall better for the statistic
            for country in avgZScore:
                avgZScore[country]=-1*avgZScore[country]
        for country in avgZScore:
            finalScores[country].append(avgZScore[country])
    for country in finalScores:
        finalAvgScores[country]=mean(finalScores[country])
    print(finalAvgScores)
    createHistogram(finalAvgScores,'Average Z Score')

#This function takes a stat and computes z scores for each country for each group (tier and tank type)
#It then averages the z scores of all the groups to get one number per country
#Returns average z score ofr each country for the inputed stat
def compareStatisticsAllTanks(statToCompare):
    allScores={'germany':[], 'usa':[], 'china':[], 'uk':[], 'other':[], 'france':[], 'ussr':[], 'japan':[]}
    avgScores={'germany':0, 'usa':0, 'china':0, 'uk':0, 'other':0, 'france':0, 'ussr':0, 'japan':0}
    possibleTiers=['1','2','3','4','5','6','7','8','9','10']
    possibleTypes=['lightTank','mediumTank','heavyTank','AT-SPG']
    for tier in possibleTiers:
        for type in possibleTypes:
            result=compareStatistics(statToCompare, tier, type)
            if bool(result)==False: #Restart loop if dictionary is empty
                continue
            if len(result)== 1: #Restart loop if only one country has tank in group (standard deviation is undefined)
                continue
            vals=list(result.values())
            if np.std(vals)==0:#Can't find z scores if standard devation is 0
                continue
            newValues=stats.zscore(vals)
            #add in z scores to lists for each country
            for i, country in enumerate(result):
                allScores[country].append(newValues[i])
    for country in allScores:
        avgScores[country]=mean(allScores[country])
    #print(statToCompare, avgScores)
    return avgScores

def main():
    getVehicleInfo()
    #Vehicle Types: mediumTank, AT-SPG, lightTank, heavyTank
    #Nations: germany, usa, china, uk, other, france, ussr, japan
    #statToCompare should be in format '[index1][index2][index3]'
    #See https://developers.wargaming.net/reference/all/wotb/encyclopedia/vehicleprofile/?application_id=demo&tank_id=14145&r_realm=na&run=1 for formating of JSON file
    statToCompare="['weight']"
    tierToCompare='10'
    typeToCompare='heavyTank'
    compareStatistics(statToCompare,tierToCompare,typeToCompare, showPlot=True)
    compareNations()

if __name__ == "__main__":
    main()

'''clan = wotb.clans.list(search='2BOOM')[0]
accounts=wotb.account.info(account_id=myID,fields='nickname')
#accounts=accounts['1012192478']['statistics']
print(accounts['1012192478']['nickname'])'''
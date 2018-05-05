#This script gets the vechicle characteristics for every tank and saves them to a dicionary then uses pickle to save them
import pickle
import wargaming
import time
import os.path
from pathlib import Path

wotb = wargaming.WoTB('demo', language='en', region='na', enable_parser=True)
tankInfo={}
allTankIDs=[]
def getVehicleInfo():
    # tankInfo is dictionary. Key is tank id and defnition is dict with keys 'name','nation', 'tier', 'type'
    global tankInfo
    tankInfo=wotb.encyclopedia.vehicles(fields=['name','nation','tier','type'])
    for tankID in tankInfo:
        allTankIDs.append(tankID)

def saveTankData():
    my_path=os.path.abspath('.\\tankData')
    print(my_path)
    for tankID in tankInfo:
        path = my_path + "\\" + str(tankID)
        my_file = Path(path)
        if my_file.is_file():
            continue
        print(path)
        while True:
            try:
                allVehicleStats = wotb.encyclopedia.vehicleprofile(tank_id=tankID)
            except:
                time.sleep(10)
                print('Request limit exceeded, waiting 10 seconds then trying again')
                continue
            else:
                break
        allVehicleStats = dict(allVehicleStats)
        pickle.dump(allVehicleStats,open(path,"wb"))
        time.sleep(5)
def main():
    getVehicleInfo()
    saveTankData()


if __name__ == "__main__":
    main()
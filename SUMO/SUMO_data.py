import sys
import optparse
import sumolib
import traci.constants as tc

import os
import time
import ray
import math
import pymysql
import sqlite3
import multiprocessing
import threading
import pandas as pd
from time import sleep

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa
# import libsumo as traci

# ray.init(address='auto', _redis_password='5241590000000000')

conn = pymysql.connect(host='34.92.132.215',user='ray',passwd='Ray@123456',database='Taskoffloading')
# conn = pymysql.connect(host='localhost',user='lwh',passwd='666888',database='Taskoffloading')
# conn = sqlite3.connect("/home/lwh/nfsroot/Taskoffload.db")
c = conn.cursor()
print ("Open database successful")

def write_sql(data: pd.DataFrame):
    # print('start')  
    for index, row in data.iterrows():
        # c.execute("REPLACE into vehicle (ID,v,angle,x,y,status) values (%s,%s,%s,%s,%s,%s)",(index,row['v'], row['angle'],row['x'],row['y'],row['status']))
        # c.execute("REPLACE into vehicle (ID,v,angle,x,y,status) values (?,?,?,?,?,?)",(index,row['v'], row['angle'],row['x'],row['y'],row['status']))
        c.execute('''insert into vehicle (ID,v,angle,x,y,status) values (%s,%s,%s,%s,%s,%s) 
                     on duplicate key update v=%s,angle=%s,x=%s,y=%s,status=%s''',(index,row['v'], row['angle'],row['x'],row['y'],row['status'],row['v'], row['angle'],row['x'],row['y'],row['status']))
    conn.commit()
    # print('com')

def run():
    """execute the TraCI control loop"""
    step = 0
    times = 0
    # we start with phase 2 where EW has green
    traci.trafficlight.setPhase("0", 2)

    po = multiprocessing.Pool(1)
    exchange = pd.DataFrame({'v':[],
                            'angle':[],
                            'x':[],
                            'y':[],
                            'status':[]},
                            index=[])

    time_start = time.time()
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if traci.trafficlight.getPhase("0") == 2:
            # we are not already switching
            if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
                # there is a vehicle from the north, switch
                traci.trafficlight.setPhase("0", 3)
            else:
                # otherwise try to keep green for EW
                traci.trafficlight.setPhase("0", 2)

        exchange.loc[:,'status'] = 'stop'
        IDlist = traci.vehicle.getIDList()
        for name in IDlist:
            exchange.loc[name,['v','angle','x','y','status']] = [traci.vehicle.getSpeed(name),
                                                                traci.vehicle.getAngle(name),
                                                                traci.vehicle.getPosition(name)[0],
                                                                traci.vehicle.getPosition(name)[1],
                                                                'run']
        if times == 0:
            # po.apply_async(write_sql,(exchange,))
            write_sql(exchange)
            times = 3
        step += 1
        times -= 1
    po.apply_async(write_sql,(exchange,))
    po.close()
    po.join()
    time_end = time.time()
    total_time = time_end - time_start
    print("Total time is: %f" %(total_time))

    traci.close()
    sys.stdout.flush()

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

# task_csv()

if __name__ == "__main__":
    options = get_options()
    
    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # net = sumolib.net.readNet("traci_tls/data/cross.net.xml")
    # print(net.getNode('51').getCoord())
    # nextNodeID = net.getEdge('51i').getToNode().getID()
    # print(nextNodeID)
    # first, generate the route file for this simulation
    # generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "traci_tls/data/cross.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    
    run()

    conn.close()
    print ("Close database")


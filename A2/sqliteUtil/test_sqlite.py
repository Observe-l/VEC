from sqliteUtil.BSSqliteUtil import *

import numpy as np

def insert_data():
    baseStations = [BaseStation() for i in range(10)]
    for i in range(len(baseStations)):
        baseStations[i].id = i
        baseStations[i].global_computing_resource = np.random.uniform(20, 29)
        baseStations[i].reversed_computing_resource = np.random.uniform(0,10)
        baseStations[i].completion_ratio = 0
        baseStations[i].computing_efficiency = 0
        baseStations[i].total_received_task = 0
        baseStations[i].reliability = 0
        insert(baseStations[i])
    print("successfully insert database")
    return baseStations




if __name__ == '__main__':

    #insert data
    BSs = insert_data()


    # #select data
    # bs1 = selectById(1)
    #
    # #update data
    # bs1.total_received_task+=1
    # update(bs1.id,bs1)
    #
    # bs = selectAll()
    # print("hhh")









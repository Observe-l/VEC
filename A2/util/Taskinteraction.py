import datetime
# from util.TaskTransfer import TaskDF2Task
from Task import Task
import pandas as pd
import json
import numpy as np
import time
from TaskBlochain import taskBlockchain
class taskInteraction():
    def __init__(self):
        self.bchain=taskBlockchain()
    def insert(self,task:Task):
        self.bchain.update(task)
        return

    def countAllByBS(self, basestationId):
        tasklist=self.bchain.getAllTask()
        count=0
        for i,v in enumerate(tasklist):
            if v.allocation_basestation_id==basestationId:
                count+=1
        return count

    def countDoneByBS(self, basestationId):
        tasklist=self.bchain.getAllTask()
        count=0
        for i,v in enumerate(tasklist):
            if v.allocation_basestation_id==basestationId and v.done_status==1:
                count+=1
        return count

    def getNowTimestamp(self):
        now=datetime.datetime.now()
        ts = now.strftime('%Y%m%d%H%M%S')
        # print(ts)
        return ts


    def selectLatest(self, sk, ek):
        tasklist=self.bchain.getAllTask(sk, ek)
        if tasklist==0:
            return 0
        count=0
        newlist=[]
        for i,v in enumerate(tasklist):
            newlist.append(v)
        return newlist

    def countAll(self):
        tasklist=self.bchain.getAllTask()
        return len(tasklist)
    def getFirstId(self):
        tasklist=self.bchain.getAllTask()
        # print("select data successfully")
        return tasklist[0].id

    def getLastId(self):
        tasklist=self.bchain.getAllTask()
        # print("select data successfully")
        return tasklist[-1].id

    def deleteAllTasks(self):
        self.bchain.delAllTask()
        return
    
    def selectAllTasks(self):
        tasklist=self.bchain.getAllTask()
        newlist=[]
        for i,v in enumerate(tasklist):
            newlist.append(v)
        return newlist



if __name__ == '__main__':
    tbc=taskInteraction()
    # createDB()
    # ID=getFirstId()
    # print(ID)
    # task1 = selectLatest(1)
    # print(task1[0].vehicle_density[str(1)])
    # a = np.array([task1[0].vehicle_density[str(i+1)] for i in range(2)])
    # print(a)
    # task=Task()
    # task.id="456"
    # task.offload_vehicle_id =  567
    # task.service_vehicle_id = 9877
    # task.allocation_basestation_id = 2
    # task.done_status = 1
    # task.vehicle_density = "{2:3, 1:2}"
    # task.delay = 5
    # tbc.insert(task)
    # print(tbc.deleteAllTasks())
    l1=tbc.selectAllTasks()
    print(len(l1))

    





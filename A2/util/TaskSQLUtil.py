import datetime
import pymysql
import sys
sys.path.append("..")
from util.TaskTransfer import TaskDF2Task
from util.Task import Task
import pandas as pd
import json
import numpy as np

def insert(task:Task):
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')
    cursor = conn.cursor()

    vehicle_density = json.dumps(task.vehicle_density)

    sql = "INSERT INTO TASK (offload_vehicle_id,\
        service_vehicle_id,allocation_basestation_id,delay,done_status,vehicle_density) VALUES ( "+str(task.offload_vehicle_id) + " ," \
          + str(task.service_vehicle_id) + " ," + str(task.allocation_basestation_id) + " ,"+str(task.delay)+"," \
          + str(task.done_status) +",\'"+vehicle_density+ "\');"
    print(sql)
    # 执行sql语句
    cursor.execute(sql)
    # 执行sql语句
    conn.commit()
    # 关闭数据库连接
    conn.close()
    return

def countAllByBS(basestation_id):
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    command = "SELECT * FROM TASK where allocation_basestation_id="+str(basestation_id)+";"
    data = pd.read_sql(command, conn)
    count=data.shape[0]
    conn.close()
    # print("select data successfully")
    return count

def countDoneByBS(basestation_id):
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    command = "SELECT * FROM TASK where allocation_basestation_id=" + str(basestation_id) + " and done_status=1;"
    data = pd.read_sql(command, conn)
    count = data.shape[0]
    conn.close()
    # print("select data successfully")
    return count


# def deleteAll():
#     # conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
#     conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

#     c = conn.cursor()
#     command = "DELETE from TASK"
#     c.execute(command)
#     conn.commit()
#     conn.close()
#     # print("delete the table data")
#     return


def createDB():
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c=conn.cursor()
    command = "CREATE TABLE TASK( id MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
            offload_vehicle_id REAL,\
            service_vehicle_id REAL,\
            allocation_basestation_id INT,\
            delay REAL,\
            done_status TINYINT,\
            vehicle_density VARCHAR(40));"
    cursor=c.execute(command)
    conn.commit()
    conn.close()
    print("create database successfully")
    return


def getNowTimestamp():
    now=datetime.datetime.now()
    ts = now.timestamp()
    return ts


def selectLatest(num):
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    command = "SELECT * FROM TASK ORDER BY id DESC LIMIT "+str(num)+";"
    data = pd.read_sql(command, conn)
    conn.close()
    tasks = TaskDF2Task(data)
    return tasks

def countAll():
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    command = "SELECT * FROM TASK;"
    data = pd.read_sql(command, conn)
    count = data.shape[0]
    conn.close()
    # print("select data successfully")
    return count

def getFirstId():
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    command = "SELECT id FROM TASK limit 1;"
    data = pd.read_sql(command, conn)
    if data.shape[0]==0:
        return 0
    id = data.iloc[0,0]
    conn.close()
    # print("select data successfully")
    return id

def getLastId():
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    command = "SELECT id FROM TASK ORDER BY id DESC LIMIT 1;"
    data = pd.read_sql(command, conn)
    if data.shape[0]==0:
        return 0
    id = data.iloc[0, 0]
    conn.close()
    # print("select data successfully")
    return id

def deleteAllTasks():
    # conn = pymysql.connect(host='34.92.132.215', user='ray', passwd='Ray@123456', database='basestation')
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    command = "DELETE from TASK"
    c.execute(command)
    conn.commit()
    conn.close()
    # print("delete the table data")
    return


if __name__ == '__main__':
    # createDB()
    ID=getFirstId()
    print(ID)
    # task1 = selectLatest(1)
    # print(task1[0].vehicle_density[str(1)])
    # a = np.array([task1[0].vehicle_density[str(i+1)] for i in range(2)])
    # print(a)




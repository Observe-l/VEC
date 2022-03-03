import datetime
import pymysql
from util.TaskTransfer import TaskDF2Task
from util.Task import Task
import pandas as pd
import json

def insert(task:Task):
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')
    cursor = conn.cursor()

    vehicle_density = json.dumps(task.vehicle_density)

    sql = "INSERT INTO TASK (id,offload_vehicle_id,\
        service_vehicle_id,allocation_basestation_id,allocation_begin_time,allocation_end_time,done_status,vehicle_density) VALUES (" + str(
        task.id) + " ," + str(task.offload_vehicle_id) + " ," \
          + str(task.service_vehicle_id) + " ," + str(task.allocation_basestation_id) + " ,now(3),now(3)," \
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
    command = "CREATE TABLE TASK( id VARCHAR(20) PRIMARY KEY NOT NULL,\
            offload_vehicle_id REAL,\
            service_vehicle_id REAL,\
            allocation_basestation_id REAL,\
            allocation_begin_time TIMESTAMP(3),\
            allocation_end_time TIMESTAMP(3) DEFAULT '2022-02-22 19:41:11.524',\
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


if __name__ == '__main__':
    task = Task()
    task.allocation_basestation_id=1
    task.done_status=1
    task.id=1
    task.offload_vehicle_id=1
    task.service_vehicle_id=2
    task.vehicle_density = {'0':4,'1':24}
    insert(task)
    # task = selectLatest(1)
    # print("1")



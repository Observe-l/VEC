import datetime
import pymysql
from A2.util.TaskTransfer import TaskDF2Task
from A2.util.Task import Task
import pandas as pd

def insert(task:Task):
    # conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')
    cursor = conn.cursor()
    # sql = "INSERT INTO TASK (id,offload_vehicle_id,\
    # service_vehicle_id,allocation_basestation_id,allocation_begin_time,allocation_end_time,done_status) VALUES ("+str(task.id)+" ,"+str(task.offload_vehicle_id)+" ,"\
    #           +str(task.service_vehicle_id)+" ,"+str(task.allocation_basestation_id)+" ,"+str(task.allocation_begin_time)+","+str(task.allocation_end_time)+"," \
    #           +str(task.done_status)+");"

    sql = "INSERT INTO TASK (id,offload_vehicle_id,\
        service_vehicle_id,allocation_basestation_id,allocation_begin_time,allocation_end_time,done_status) VALUES (" + str(
        task.id) + " ," + str(task.offload_vehicle_id) + " ," \
          + str(task.service_vehicle_id) + " ," + str(task.allocation_basestation_id) + " ,now(3),now(3)," \
          + str(task.done_status) + ");"
    print(sql)
    # 执行sql语句
    cursor.execute(sql)
    # 执行sql语句
    conn.commit()

    # 关闭数据库连接
    conn.close()
    return

def countAllByBS(basestation_id):
    # conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    command = "SELECT * FROM TASK where allocation_basestation_id="+str(basestation_id)+";"
    data = pd.read_sql(command, conn)
    count=data.shape[0]
    conn.close()
    # print("select data successfully")
    return count

def countDoneByBS(basestation_id):
    # conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    command = "SELECT * FROM TASK where allocation_basestation_id=" + str(basestation_id) + " and done_status=1;"
    data = pd.read_sql(command, conn)
    count = data.shape[0]
    conn.close()
    # print("select data successfully")
    return count


def deleteAll():
    # conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    command = "DELETE from TASK"
    c.execute(command)
    conn.commit()
    conn.close()
    # print("delete the table data")
    return


def createDB():
    # conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c=conn.cursor()
    command = "CREATE TABLE TASK( id VARCHAR(20) PRIMARY KEY NOT NULL,\
            offload_vehicle_id REAL,\
            service_vehicle_id REAL,\
            allocation_basestation_id REAL,\
            allocation_begin_time TIMESTAMP(3),\
            allocation_end_time TIMESTAMP(3) DEFAULT '2022-02-22 19:41:11.524',\
            done_status TINYINT);"
    cursor=c.execute(command)
    conn.commit()
    conn.close()
    print("create database successfully")
    return


def getNowTimestamp():
    now=datetime.datetime.now()
    ts = now.timestamp()
    return ts

    # def selectById(id):
    #     # conn = pymysql.connect(host='localhost',port=3307,user='root',password='root',db='VEC.db')
    #     conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    #     c = conn.cursor()
    #     command = "SELECT * from BASESTATION WHERE id=" + str(id)
    #     cursor = c.execute(command)
    #     bs = BaseStation()
    #     for row in cursor:
    #         bs.id = row[0]
    #         bs.global_computing_resource = row[1]
    #         bs.reversed_computing_resource = row[2]
    #         bs.computing_efficiency = row[3]
    #         bs.completion_ratio = row[4]
    #         bs.total_received_task = row[5]
    #         bs.reliability = row[6]
    #     conn.close()
    #     # print("select data successfully")
    #     return bs

def selectLatest(num):
    # conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    command = "SELECT * FROM TASK ORDER BY id DESC LIMIT "+str(num)+";"
    data = pd.read_sql(command, conn)
    conn.close()
    tasks = TaskDF2Task(data)
    return tasks

    #     bs = BaseStation()
    #     for row in cursor:
    #         bs.id = row[0]
    #         bs.global_computing_resource = row[1]
    #         bs.reversed_computing_resource = row[2]
    #         bs.computing_efficiency = row[3]
    #         bs.completion_ratio = row[4]
    #         bs.total_received_task = row[5]
    #         bs.reliability = row[6]
    #     conn.close()
    #     # print("select data successfully")
    #     return bs

def countAll():
    # conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    command = "SELECT * FROM TASK;"
    data = pd.read_sql(command, conn)
    count = data.shape[0]
    conn.close()
    # print("select data successfully")
    return count





if __name__ == '__main__':
    # createDB()

    #load 2 tasks
    # deleteAll()
    # task1=Task()
    # task1.id=3
    # task1.offload_vehicle_id=1
    # task1.allocation_begin_time=getNowTimestamp()-100
    # task1.allocation_end_time=getNowTimestamp()
    # task1.done_status=1
    # task1.allocation_basestation_id=1
    # task1.service_vehicle_id=2
    #
    # task2=Task()
    # task2.id=4
    # task2.offload_vehicle_id = 2
    # task2.allocation_begin_time = getNowTimestamp()
    # task2.allocation_end_time = getNowTimestamp()
    # task2.done_status = 0
    # task2.allocation_basestation_id = 2
    # task2.service_vehicle_id = 1
    # insert(task1)
    # insert(task2)

    # temp=countAllByBS(2)
    # print(temp)
    tasks = selectLatest(1)
    print("hh")

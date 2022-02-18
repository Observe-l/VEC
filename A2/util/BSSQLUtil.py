import pymysql
from A2.util.BaseStation import BaseStation
from A2.util.BaseStationTransfer import *
import pandas as pd

def insert(bs:BaseStation):
    # conn = pymysql.connect(host='34.92.132.215', user='ray', passwd='Ray@123456', database='basestation')
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    cursor = conn.cursor()
    sql = "INSERT INTO BASESTATION (id,global_computing_resource,\
    reversed_computing_resource,computing_efficiency,completion_ratio,\
    total_received_task,reliability) VALUES ("+str(bs.id)+" ,"+str(bs.global_computing_resource)+" ,"\
              +str(bs.reversed_computing_resource)+" ,"+str(bs.computing_efficiency)+" ,"\
              +str(bs.completion_ratio)+" ,"+str(bs.total_received_task)+" ,"+str(bs.reliability)+")"
    try:
        # 执行sql语句
        # print(sql)
        cursor.execute(sql)
        # 执行sql语句
        conn.commit()
    except:
        # 发生错误时回滚
        print("error")
        conn.rollback()

    # 关闭数据库连接
    conn.close()
    return

def selectById(id):
    # conn = pymysql.connect(host='localhost',port=3307,user='root',password='root',db='VEC.db')
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    c = conn.cursor()
    command = "SELECT * from BASESTATION WHERE id="+str(id)
    cursor = c.execute(command)
    bs = BaseStation()
    for row in cursor:
        bs.id = row[0]
        bs.global_computing_resource = row[1]
        bs.reversed_computing_resource = row[2]
        bs.computing_efficiency = row[3]
        bs.completion_ratio = row[4]
        bs.total_received_task = row[5]
        bs.reliability = row[6]
    conn.close()
    # print("select data successfully")
    return bs

def selectAll():
    # conn = pymysql.connect(host='34.92.132.215', user='ray', passwd='Ray@123456', database='basestation')
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    c = conn.cursor()
    data = pd.read_sql("SELECT * from BASESTATION", conn)
    print("load all data successfully")
    return data

def update(bs):
    # conn = pymysql.connect(host='34.92.132.215', user='ray', passwd='Ray@123456', database='basestation')
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    c = conn.cursor()
    command = " UPDATE BASESTATION set global_computing_resource="+str(bs.global_computing_resource)\
        +",reversed_computing_resource="+str(bs.reversed_computing_resource)\
        +",computing_efficiency="+str(bs.computing_efficiency) \
        +",completion_ratio=" + str(bs.completion_ratio) \
        +",total_received_task=" + str(bs.total_received_task) \
        +",reliability=" + str(bs.reliability)+" where id="+str(bs.id)
    cursor = c.execute(command)
    conn.commit()
    conn.close()
    # print("update data  successfully")
    return bs

def deleteAll():
    # conn = pymysql.connect(host='34.92.132.215', user='ray', passwd='Ray@123456', database='basestation')
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    c = conn.cursor()
    command = "DELETE from BASESTATION"
    c.execute(command)
    conn.commit()
    conn.close()
    # print("delete the table data")
    return

def resetDB():
    # conn = pymysql.connect(host='34.92.132.215', user='ray', passwd='Ray@123456', database='basestation')
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    c = conn.cursor()
    #initialize the base station dataframe
    data = {'id': [1, 2,3],
            'global_computing_resource': [20, 29,25],
            'reversed_computing_resource': [10, 0,5],
            'computing_efficiency': [0, 1,0.5],
            'completion_ratio': [0, 1,0],
            'total_received_task': [0, 1,0],
            'reliability': [0, 1,0.5]
            }
    df = pd.DataFrame(data)
    bss = BSDF2BS(df)
    for bs in bss:
        command = " UPDATE BASESTATION set global_computing_resource=" + str(bs.global_computing_resource) \
              + ",reversed_computing_resource=" + str(bs.reversed_computing_resource) \
              + ",computing_efficiency=" + str(bs.computing_efficiency) \
              + ",completion_ratio=" + str(bs.completion_ratio) \
              + ",total_received_task=" + str(bs.total_received_task) \
              + ",reliability=" + str(bs.reliability) + " where id=" + str(bs.id)
        cursor = c.execute(command)
    conn.commit()
    conn.close()
    # print("update data  successfully")
    return bs

def createDB():
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    c=conn.cursor()
    command = "CREATE TABLE BASESTATION( id VARCHAR(20) PRIMARY KEY NOT NULL,\
             global_computing_resource REAL,\
            reversed_computing_resource REAL,\
            computing_efficiency REAL,\
            completion_ratio REAL,\
            total_received_task REAL,\
            reliability REAL);"
    cursor=c.execute(command)
    conn.commit()
    conn.close()
    print("create database successdully")
    return

def initializeDB():
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    c = conn.cursor()
    # initialize the base station dataframe
    data = {'id': [1, 2,3],
            'global_computing_resource': [20, 29,25],
            'reversed_computing_resource': [10, 0,5],
            'computing_efficiency': [0, 1,0.5],
            'completion_ratio': [0, 1,0],
            'total_received_task': [0, 1,0],
            'reliability': [0, 1,0.5]
            }
    df = pd.DataFrame(data)
    bss = BSDF2BS(df)
    for bs in bss:
        command = " insert into BASESTATION (id,global_computing_resource,\
        reversed_computing_resource,computing_efficiency,\
        completion_ratio,total_received_task,reliability) \
        values ("+str(bs.id)+\
        ","+str(bs.global_computing_resource)+ \
        ","+str(bs.reversed_computing_resource) +\
        ","+str(bs.computing_efficiency)+\
        ","+str(bs.completion_ratio)+\
        ","+str(bs.total_received_task) +\
        ","+str(bs.reliability)+");"
        cursor = c.execute(command)
    conn.commit()
    conn.close()
    print("initialize data successfully")
    return bs



if __name__ == '__main__':
     bs = BaseStation()
     bs.id = 3
     bs.global_computing_resource=25
     bs.reversed_computing_resource=5
     bs.computing_efficiency=0.5
     bs.completion_ratio=0.5
     bs.total_received_task = 0
     bs.reliability=0.5
     insert(bs)




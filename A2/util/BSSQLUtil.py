import pymysql
import sys
sys.path.append("..")
from util.BaseStation import BaseStation
from util.BaseStationTransfer import *
import pandas as pd

def insert(bs:BaseStation):
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    cursor = conn.cursor()
    sql = "INSERT INTO BASESTATION (id,global_computing_resource,\
    reserved_computing_resource,vehicle_density,computing_efficiency,completion_ratio,\
    total_received_task,reliability) VALUES ("+str(bs.id)+" ,"+str(bs.global_computing_resource)+" ,"\
              +str(bs.reserved_computing_resource)+" ,"+str(bs.vehicle_density)+","+str(bs.computing_efficiency)+" ,"\
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
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    data = pd.read_sql("SELECT * from BASESTATION WHERE id="+str(id), conn)
    bss = BSDF2BS(data)
    # print("select data successfully")
    return bss[0]

def selectAll():
    # conn = pymysql.connect(host='34.92.132.215', user='ray', passwd='Ray@123456', database='basestation')
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    data = pd.read_sql("SELECT * from BASESTATION", conn)
    conn.close()
    print("load all data successfully")
    return data

def update(bs):
    # conn = pymysql.connect(host='34.92.132.215', user='ray', passwd='Ray@123456', database='basestation')
    conn = pymysql.connect(host='localhost', user='VEC', passwd='666888', database='DDQN')
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    command = " UPDATE BASESTATION set global_computing_resource="+str(bs.global_computing_resource)\
        +",reserved_computing_resource="+str(bs.reserved_computing_resource)\
        +",vehicle_density="+str(bs.vehicle_density) \
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
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

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
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c = conn.cursor()
    #initialize the base station dataframe
    data = {'id': [1, 2],
            'global_computing_resource': [20, 29],
            'reserved_computing_resource': [10, 0],
            'vehicle_density':[40,5],
            'computing_efficiency': [0, 0],
            'completion_ratio': [0, 0],
            'total_received_task': [0, 0],
            'reliability': [0, 0]
            }
    df = pd.DataFrame(data)
    bss = BSDF2BS(df)
    for bs in bss:
        command = " UPDATE BASESTATION set global_computing_resource=" + str(bs.global_computing_resource) \
              + ",reserved_computing_resource=" + str(bs.reserved_computing_resource) \
              +",vehicle_density="+str(bs.vehicle_density)\
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
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')

    c=conn.cursor()
    command = "CREATE TABLE BASESTATION( id VARCHAR(20) PRIMARY KEY NOT NULL,\
             global_computing_resource REAL,\
            reserved_computing_resource REAL, \
            vehicle_density REAL, \
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
    # conn = pymysql.connect(host='localhost', user='database', passwd='123456', database='basestation')
    c = conn.cursor()
    # initialize the base station dataframe
    data = {'id': [1, 2],
            'global_computing_resource': [20, 29],
            'reserved_computing_resource': [10, 0],
            'vehicle_density':[40,5],
            'computing_efficiency': [0, 1],
            'completion_ratio': [0, 1],
            'total_received_task': [0, 1],
            'reliability': [0, 1]
            }
    df = pd.DataFrame(data)
    bss = BSDF2BS(df)
    for bs in bss:
        command = " insert into BASESTATION (id,global_computing_resource,\
        reserved_computing_resource,vehicle_density,computing_efficiency,\
        completion_ratio,total_received_task,reliability) \
        values ("+str(bs.id)+\
        ","+str(bs.global_computing_resource)+ \
        ","+str(bs.reserved_computing_resource) +\
        ","+str(bs.vehicle_density)+\
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
    # createDB()
    initializeDB()




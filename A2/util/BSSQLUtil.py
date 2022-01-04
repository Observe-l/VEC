import pymysql
from util.BaseStation import BaseStation
import pandas as pd

def insert(bs:BaseStation):
    conn = pymysql.connect(host='34.92.132.215', user='ray', passwd='Ray@123456', database='basestation')
    # conn = pymysql.connect(host='localhost',user='root',password='root',db='VEC.db')
    cursor = conn.cursor()
    sql = "INSERT INTO BASESTATION (id,global_computing_resource,\
    reversed_computing_resource,computing_efficiency,completion_ratio,\
    total_received_task,reliability) VALUES ("+str(bs.id)+" ,"+str(bs.global_computing_resource)+" ,"\
              +str(bs.reversed_computing_resource)+" ,"+str(bs.computing_efficiency)+" ,"\
              +str(bs.completion_ratio)+" ,"+str(bs.total_received_task)+" ,"+str(bs.reliability)+")"
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        conn.commit()
    except:
        # 发生错误时回滚
        conn.rollback()

    # 关闭数据库连接
    conn.close()
    return

def selectById(id):
    conn = pymysql.connect(host='localhost',port=3307,user='root',password='root',db='VEC.db')
    # conn = pymysql.connect(host='localhost',user='root',password='root',db='VEC.db')
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
    conn = pymysql.connect(host='34.92.132.215', user='ray', passwd='Ray@123456', database='basestation')
    # conn = pymysql.connect(host='localhost',port=3307,user='root',password='root',db='VEC.db')
    c = conn.cursor()
    # command = "SELECT * from BASESTATION"
    # cursor = c.execute(command)
    # baseStations = []
    # for row in cursor:
    #     bs = BaseStation()
    #     bs.id = row[0]
    #     bs.global_computing_resource = row[1]
    #     bs.reversed_computing_resource = row[2]
    #     bs.computing_efficiency = row[3]
    #     bs.completion_ratio = row[4]
    #     bs.total_received_task = row[5]
    #     bs.reliability = row[6]
    #     baseStations.append(bs)
    # conn.close()
    data = pd.read_sql("SELECT * from BASESTATION", conn)
    print("load all data successfully")
    return data

def update(id,bs):
    conn = pymysql.connect(host='34.92.132.215', user='ray', passwd='Ray@123456', database='basestation')
    # conn = pymysql.connect(host='localhost',user='root',password=',db='VEC.db')
    c = conn.cursor()
    command = " UPDATE BASESTATION set global_computing_resource="+str(bs.global_computing_resource)\
        +",reversed_computing_resource="+str(bs.reversed_computing_resource)\
        +",computing_efficiency="+str(bs.computing_efficiency) \
        +",completion_ratio=" + str(bs.completion_ratio) \
        +",total_received_task=" + str(bs.total_received_task) \
        +",reliability=" + str(bs.reliability)+" where id="+str(id)
    cursor = c.execute(command)
    conn.commit()
    conn.close()
    # print("update data  successfully")
    return bs

def deleteAll():
    # conn = pymysql.connect(host='34.92.132.215', user='ray', passwd='Ray@123456', database='basestation')
    conn = pymysql.connect(host='localhost',user='root',password='root',db='VEC.db')
    c = conn.cursor()
    command = "DELETE from BASESTATION"
    c.execute(command)
    conn.commit()
    conn.close()
    # print("delete the table data")
    return

def resetDB():
    conn = pymysql.connect(host='34.92.132.215', user='ray', passwd='Ray@123456', database='basestation')
    # conn = pymysql.connect(host='localhost',user='root',password=',db='VEC.db')
    c = conn.cursor()
    command = " UPDATE BASESTATION set global_computing_resource=" + str(bs.global_computing_resource) \
              + ",reversed_computing_resource=" + str(bs.reversed_computing_resource) \
              + ",computing_efficiency=" + str(bs.computing_efficiency) \
              + ",completion_ratio=" + str(bs.completion_ratio) \
              + ",total_received_task=" + str(bs.total_received_task) \
              + ",reliability=" + str(bs.reliability) + " where id=" + str(id)
    cursor = c.execute(command)
    conn.commit()
    conn.close()
    # print("update data  successfully")
    return bs


if __name__ == '__main__':
    bs = BaseStation()
    # bs.global_computing_resource=
    update(1)
    bs = selectAll()
    print(bs)

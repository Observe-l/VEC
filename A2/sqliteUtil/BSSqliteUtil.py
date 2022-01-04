import sqlite3
from model.BaseStation import BaseStation
path = '/home/jaimin/VEC.db'
conn = sqlite3.connect(path)


def insert(bs:BaseStation):
    c = conn.cursor()
    command = "INSERT INTO BASESTATION (id,global_computing_resource,\
    reversed_computing_resource,computing_efficiency,completion_ratio,\
    total_received_task,reliability) VALUES ("+str(bs.id)+" ,"+str(bs.global_computing_resource)+" ,"\
              +str(bs.reversed_computing_resource)+" ,"+str(bs.computing_efficiency)+" ,"\
              +str(bs.completion_ratio)+" ,"+str(bs.total_received_task)+" ,"+str(bs.reliability)+")"
    c.execute(command)
    c.commit()
    c.close()
    return

def selectById(id):
    conn =sqlite3.connect(path)
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
    conn = sqlite3.connect(path)
    c = conn.cursor()
    command = "SELECT * from BASESTATION"
    cursor = c.execute(command)
    baseStations = []
    for row in cursor:
        bs = BaseStation()
        bs.id = row[0]
        bs.global_computing_resource = row[1]
        bs.reversed_computing_resource = row[2]
        bs.computing_efficiency = row[3]
        bs.completion_ratio = row[4]
        bs.total_received_task = row[5]
        bs.reliability = row[6]
        baseStations.append(bs)
    conn.close()
    # print("load all data successfully")
    return baseStations

def update(id,bs):
    conn = sqlite3.connect(path)
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
    conn = sqlite3.connect(path)
    c = conn.cursor()
    command = "DELETE from BASESTATION"
    c.execute(command)
    conn.commit()
    conn.close()
    # print("delete the table data")
    return

if __name__ == '__main__':
    bs = BaseStation();






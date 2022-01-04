import pymysql
from model.BaseStation import BaseStation

def insert(bs:BaseStation):
    db = pymysql.connect(host='34.92.132.215', user='ray', passwd='Ray@123456', database='basestation')
    cursor = db.cursor()
    sql = "INSERT INTO BASESTATION (id,global_computing_resource,\
    reversed_computing_resource,computing_efficiency,completion_ratio,\
    total_received_task,reliability) VALUES ("+str(bs.id)+" ,"+str(bs.global_computing_resource)+" ,"\
              +str(bs.reversed_computing_resource)+" ,"+str(bs.computing_efficiency)+" ,"\
              +str(bs.completion_ratio)+" ,"+str(bs.total_received_task)+" ,"+str(bs.reliability)+")"
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    db.close()
    return

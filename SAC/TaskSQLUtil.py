from Task import Task
import pymysql
import json

def insert(task:Task):
  conn = pymysql.connect(host='192.168.1.117', user='VEC', passwd='666888', database='DDQN')
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
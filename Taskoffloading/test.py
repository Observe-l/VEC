import pymysql
import ray
import os
import socket
import struct

from time import time
def get_ip():
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()
    return ip

# ray.init(address='auto', _redis_password='5241590000000000')

# conn = pymysql.connect(host='localhost',user='lwh',passwd='666888',database='Taskoffloading')
# c = conn.cursor()
# print ("Open database successful")

# dd = pd.read_sql("SELECT * FROM vehicle",conn,index_col='ID')
# # print(dd)
# dd.to_csv('test.csv')
# conn.close()
# print ("Close database")
start_time=time()
ip = get_ip()
print(ip)
print(type(ip))
sk = socket.socket(type=socket.SOCK_DGRAM)
stri1 = 'send'
mesg = struct.pack('!20si20s',stri1.encode(),8000,b'task_file')
sk.sendto(mesg,("192.168.31.196",4563))
end_time=time()
print("Total time: ",end_time-start_time)
print(start_time)
print(str(start_time))
# print(type(start_time))

sk.close()
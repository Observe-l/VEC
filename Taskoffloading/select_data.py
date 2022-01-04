import sqlite3
import pymysql
import time
import pandas as pd

# conn = pymysql.connect(host='34.92.132.215',user='ray',passwd='Ray@123456',database='Taskoffloading')
# conn = pymysql.connect(host='localhost',user='lwh',passwd='666888',database='Taskoffloading')
conn = pymysql.connect(host='192.168.31.196',user='lwh_sql',passwd='666888',database='Taskoffloading')
# conn = sqlite3.connect("/home/lwh/nfsroot/Taskoffload.db")
c = conn.cursor()
print ("Open database successful")
while 1:
    a = input("\nNote:\n[1] Print all data\n[2] Select data\n[3] Exit\n")
    if a=="1":
        time_start = time.time()
        conn.commit()
        dd = pd.read_sql("SELECT * FROM vehicle",conn)
        time_end = time.time()
        total_time = time_end - time_start
        print("Total time is:", total_time,"seconds")
        print(dd)
    if a=="2":
        command=input("Please input ID:")
        time_start = time.time()
        conn.commit()
        dd = pd.read_sql("SELECT * FROM vehicle where ID = %(index)s",conn,params={'index': command})
        time_end = time.time()
        total_time = time_end - time_start
        print("Total time is:", total_time,"seconds")
        print(dd)   
    elif a=="3":
        break

conn.close()
print ("Close database")

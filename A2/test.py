import pandas as pd
import pymysql

conn=pymysql.connect(host='34.92.132.215',user='ray',passwd='Ray@123456',database='Taskoffloading')
data = pd.read_sql("SELECT * from vehicle",conn)
conn.close()
print(data)

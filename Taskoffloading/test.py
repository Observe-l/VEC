import sqlalchemy
import pymysql
import pandas as pd
import ray
import os
import socket
import struct

# engin = sqlalchemy.create_engine('mysql+pymysql://lwh:666888@localhost/SAC')
conn = pymysql.connect(host='localhost',user='lwh',passwd='666888',database='SAC')

c = conn.cursor()
# conn = engin.connect()

sql_cmd = "select * from vehicle_information"
a = '1'

while a == '1':
    data_test = pd.read_sql(sql_cmd,conn)
    print(data_test)
    a=input("1: next; other: exit\n")
    # conn = engin.connect()
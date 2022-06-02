import pymysql

''' 
Assume Vehicle 0 as Task Vehicle 
-------------------------------------------------------------------------------------
| EVENT | send_time | Vehicle 1 | Vehicle 2| Vehicle 3| BS0_DENSITY |BS1_DENSITY|
|   1   |    64     |   1.23    |  0.81    |   0.43   |     4       |    0      |
...
--------------------------------------------------------------------------------------
'''

db = pymysql.connect(
     host = "192.168.1.117",
     user = "VEC",
     password = "666888",
     database = "SAC",
)

cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS ts_vehicle0")
cursor.execute("DROP TABLE IF EXISTS ts_vehicle1")
cursor.execute("DROP TABLE IF EXISTS ts_vehicle2")
cursor.execute("DROP TABLE IF EXISTS ts_vehicle3")

# create table 0: ts_vehicle0
sql = """CREATE TABLE ts_vehicle0 (
         EVENT varchar(255),
         SEND_TIME  int,
         VEHICLE1 FLOAT,
         VEHICLE2 FLOAT,  
         VEHICLE3 FLOAT,
         BS0_DENSITY int,
         BS1_DENSITY int)"""
cursor.execute(sql)

# create table 1: ts_vehicle1
sql = """CREATE TABLE ts_vehicle1 (
         EVENT varchar(255),
         SEND_TIME  int,
         VEHICLE0 FLOAT,
         VEHICLE2 FLOAT,  
         VEHICLE3 FLOAT,
         BS0_DENSITY int,
         BS1_DENSITY int)"""
cursor.execute(sql)

# create table 2: ts_vehicle2
sql = """CREATE TABLE ts_vehicle2 (
         EVENT varchar(255),
         SEND_TIME  int,
         VEHICLE0 FLOAT,
         VEHICLE1 FLOAT,  
         VEHICLE3 FLOAT,
         BS0_DENSITY int,
         BS1_DENSITY int)"""
cursor.execute(sql)

# create table 3: ts_vehicle3
sql = """CREATE TABLE ts_vehicle3 (
         EVENT varchar(255),
         SEND_TIME  int,
         VEHICLE0 FLOAT,
         VEHICLE1 FLOAT,  
         VEHICLE2 FLOAT,
         BS0_DENSITY int,
         BS1_DENSITY int)"""
cursor.execute(sql)

# insert data into tabel0
sql = """INSERT INTO ts_vehicle0(
         EVENT, SEND_TIME, VEHICLE1, VEHICLE2, VEHICLE3, BS0_DENSITY, BS1_DENSITY)
         VALUES (1,  64,     1.23,  0.81,   0.43, 4, 0);"""
cursor.execute(sql)
db.commit()

# insert data into table1
sql = """INSERT INTO ts_vehicle1(
         EVENT, SEND_TIME, VEHICLE0, VEHICLE2, VEHICLE3, BS0_DENSITY, BS1_DENSITY)
         VALUES (1, 64,    1.23,   0.67,  0.57, 4, 0);"""
cursor.execute(sql)
db.commit()

# insert data into table2
sql = """INSERT INTO ts_vehicle2(
         EVENT, SEND_TIME, VEHICLE0, VEHICLE1, VEHICLE3, BS0_DENSITY, BS1_DENSITY)
         VALUES (1, 64,     0.81,  0.67,   0.27, 4, 0);"""
cursor.execute(sql)
db.commit()

# insert data into table3
sql = """INSERT INTO ts_vehicle3(
         EVENT, SEND_TIME, VEHICLE0, VEHICLE1, VEHICLE2, BS0_DENSITY, BS1_DENSITY)
         VALUES (1, 64,     0.43,    0.57,   0.27, 4, 0);"""
cursor.execute(sql)
db.commit()

db.close()
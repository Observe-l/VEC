import pymysql

''' 
Assume Vehicle 0 as Task Vehicle 
-------------------------------------------------------------------------------------
|event | send_time | Vehicle 0->Vehicle 1 | Vehicle 0->Vehicle 2| Vehicle 0->Vehicle 3|
|  1   |    64     |         1.23         |         0.81        |         0.43        |
...
--------------------------------------------------------------------------------------
'''

db = pymysql.connect(
     host = "localhost",
     user = "VEC",
     password = "666888",
     database = "SAC"
)

cursor = db.cursor()

# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS ts_vehicle0")
cursor.execute("DROP TABLE IF EXISTS ts_vehicle1")
cursor.execute("DROP TABLE IF EXISTS ts_vehicle2")
cursor.execute("DROP TABLE IF EXISTS ts_vehicle3")

# create table 0: ts_vehicle0
sql = """CREATE TABLE ts_vehicle0 (
         EVENT int,
         SEND_TIME  int,
         VEHICLE1 FLOAT,
         VEHICLE2 FLOAT,  
         VEHICLE3 FLOAT)"""
cursor.execute(sql)

# create table 1: ts_vehicle1
sql = """CREATE TABLE ts_vehicle1 (
         EVENT int,
         SEND_TIME  int,
         VEHICLE0 FLOAT,
         VEHICLE2 FLOAT,  
         VEHICLE3 FLOAT)"""
cursor.execute(sql)

# create table 2: ts_vehicle2
sql = """CREATE TABLE ts_vehicle2 (
         EVENT int,
         SEND_TIME  int,
         VEHICLE0 FLOAT,
         VEHICLE1 FLOAT,  
         VEHICLE3 FLOAT)"""
cursor.execute(sql)

# create table 3: ts_vehicle3
sql = """CREATE TABLE ts_vehicle3 (
         EVENT int,
         SEND_TIME  int,
         VEHICLE0 FLOAT,
         VEHICLE1 FLOAT,  
         VEHICLE2 FLOAT)"""
cursor.execute(sql)

# insert data into tabel0
sql = """INSERT INTO ts_vehicle0(
         EVENT, SEND_TIME, VEHICLE1, VEHICLE2, VEHICLE3)
         VALUES (1,  64,     1.23,  0.81,   0.43),
                (2,  74,     1.08,  0.68,   0.45),
                (3,  84,     2.24,  1.54,   0.8),
                (4,  94,     4.31,	2.88,	1.65),
                (5,  104,	 4.61,	4.02,	2.49),
                (6,  114,	 4.69,	4.06,	3.42),
                (7,  124,	 4.7,	4.12,	3.55),
                (8,  134,	 4.52,	3.98,	3.48),
                (9,  144,	 4.12,	3.62,	3.02),
                (10,  154,	 3.72,	3.21,	2.67),
                (11,  164,	 3.66,	2.18,	1.42),
                (12,  174,	 2.88,	2.28,	1.49),
                (13,  184,	 2.62,	1.51,	1.1),
                (14,  194,	 1.64,	1.69,	1.28);"""
cursor.execute(sql)
db.commit()

# insert data into table1
sql = """INSERT INTO ts_vehicle1(
         EVENT, SEND_TIME, VEHICLE0, VEHICLE2, VEHICLE3)
         VALUES (1, 64,    1.23,   0.67,  0.57),
                (2, 74,    1.08,   0.59,  0.94),
                (3, 84,    2.24,    1.7,  0.99),
                (4, 94,    4.31,   2.92,  1.73),
                (5, 104,   4.61,   3.97,  3.24),
                (6, 114,   4.69,    4.3,  4.05),
                (7, 124,    4.7,   4.19,  4.12),
                (8, 134,	 4.52,	4.21,	4.14),
                (9, 144,	 4.12,	4.13,	3.8),
                (10, 154,	 3.72,	3.53,	2.6),
                (11, 164,	 3.66,	3.46,	2.11),
                (12, 174,	 2.88,	2.35,	1.98),
                (13, 184,	 2.62,	2.85,	1.3),
                (14, 194,	 1.64,	2.46,	1.73);"""
cursor.execute(sql)
db.commit()

# insert data into table2
sql = """INSERT INTO ts_vehicle2(
         EVENT, SEND_TIME, VEHICLE0, VEHICLE1, VEHICLE3)
         VALUES (1, 64,     0.81,  0.67,   0.27),
                (2, 74,     0.68,  0.59,   1.59),
                (3, 84,     1.54,  1.7,     1.8),
                (4, 94,     2.88,	2.92,	3.91),
                (5, 104,	 4.02,	3.97,	4.1),
                (6, 114,	 4.06,	4.3,	4.43),
                (7, 124,	 4.12,	4.19,	4.34),
                (8, 134,	 3.98,	4.21,	4.47),
                (9, 144,	 3.62,	4.13,	3.9),
                (10,154,	 3.21,	3.53,	3.62),
                (11,164,	 2.18,	3.46,	2.59),
                (12,174,	 2.28,	2.35,	2),
                (13, 184,	 1.51,	2.85,	1.67),
                (14, 194,	 1.69,	2.46,	2.12);"""
cursor.execute(sql)
db.commit()

# insert data into table3
sql = """INSERT INTO ts_vehicle3(
         EVENT, SEND_TIME, VEHICLE0, VEHICLE1, VEHICLE2)
         VALUES (1, 64,     0.43,    0.57,   0.27),
                (2, 74,     0.45,    0.94,   1.59),
                (3, 84,      0.8,    0.99,    1.8),
                (4, 94,     1.65,    1.73,   3.91),
                (5, 104,    2.49,    3.24,    4.1),
                (6, 114,    3.42,    4.05,   4.43),
                (7, 124,    3.55,    4.12,   4.34),
                (8, 134,	 3.48,	  4.14,	  4.47),
                (9, 144,	 3.02,	   3.8,	   3.9),
                (10, 154,	 2.67,	   2.6,	  3.62),
                (11, 164,	 1.42,	  2.11,	  2.59),
                (12, 174,	 1.49,	  1.98,	     2),
                (13, 184,	  1.1,	   1.3,	  1.67),
                (14, 194,	 1.28,	  1.73,	  2.12);"""
cursor.execute(sql)
db.commit()

db.close()
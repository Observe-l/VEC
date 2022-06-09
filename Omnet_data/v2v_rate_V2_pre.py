import pymysql

''' 
-------------------------------------------------------------------------------------
|  vehicle ID  |  Vehicle 1 | Vehicle 2| Vehicle 3| ... |
|   Vehicle 1  |    .....   |    ..... |   .....  | ... |
...
--------------------------------------------------------------------------------------
'''

db = pymysql.connect(
     host = "192.168.1.122",
     user = "VEC",
     password = "666888",
     database = "SAC",
)

cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS throughput")


# create Throughput table
sql = """CREATE TABLE throughput (
         VehicleID varchar(255),
         Vehicle0 FLOAT,
         Vehicle1 FLOAT,
         Vehicle2 FLOAT,
         Vehicle3 FLOAT,
         Vehicle4 FLOAT,  
         Vehicle5 FLOAT,
         Vehicle6 FLOAT,
         Vehicle7 FLOAT,  
         Vehicle8 FLOAT,
         Vehicle9 FLOAT,
         Vehicle10 FLOAT,  
         Vehicle11 FLOAT)"""
cursor.execute(sql)

# insert data
sql = """INSERT INTO throughput(
         VehicleID, Vehicle0, Vehicle1, Vehicle2, Vehicle3, Vehicle4, Vehicle5, Vehicle6, Vehicle7, Vehicle8, Vehicle9, Vehicle10, Vehicle11)
         VALUES ('Vehicle0',  99,     12,  13,   14, 15, 16,99,     12,  13,   14, 15, 16);"""
cursor.execute(sql)

sql = """INSERT INTO throughput(
         VehicleID, Vehicle0, Vehicle1, Vehicle2, Vehicle3, Vehicle4, Vehicle5, Vehicle6, Vehicle7, Vehicle8, Vehicle9, Vehicle10, Vehicle11)
         VALUES ('Vehicle1',  99,     12,  13,   14, 15, 16,99,     12,  13,   14, 15, 16);"""
cursor.execute(sql)

sql = """INSERT INTO throughput(
         VehicleID, Vehicle0, Vehicle1, Vehicle2, Vehicle3, Vehicle4, Vehicle5, Vehicle6, Vehicle7, Vehicle8, Vehicle9, Vehicle10, Vehicle11)
         VALUES ('Vehicle2',  99,     12,  13,   14, 15, 16,99,     12,  13,   14, 15, 16);"""
cursor.execute(sql)

sql = """INSERT INTO throughput(
         VehicleID, Vehicle0, Vehicle1, Vehicle2, Vehicle3, Vehicle4, Vehicle5, Vehicle6, Vehicle7, Vehicle8, Vehicle9, Vehicle10, Vehicle11)
         VALUES ('Vehicle3',  99,     12,  13,   14, 15, 16,99,     12,  13,   14, 15, 16);"""
cursor.execute(sql)

sql = """INSERT INTO throughput(
         VehicleID, Vehicle0, Vehicle1, Vehicle2, Vehicle3, Vehicle4, Vehicle5, Vehicle6, Vehicle7, Vehicle8, Vehicle9, Vehicle10, Vehicle11)
         VALUES ('Vehicle4',  99,     12,  13,   14, 15, 16,99,     12,  13,   14, 15, 16);"""
cursor.execute(sql)

sql = """INSERT INTO throughput(
         VehicleID, Vehicle0, Vehicle1, Vehicle2, Vehicle3, Vehicle4, Vehicle5, Vehicle6, Vehicle7, Vehicle8, Vehicle9, Vehicle10, Vehicle11)
         VALUES ('Vehicle5',  99,     12,  13,   14, 15, 16,99,     12,  13,   14, 15, 16);"""
cursor.execute(sql)

sql = """INSERT INTO throughput(
         VehicleID, Vehicle0, Vehicle1, Vehicle2, Vehicle3, Vehicle4, Vehicle5, Vehicle6, Vehicle7, Vehicle8, Vehicle9, Vehicle10, Vehicle11)
         VALUES ('Vehicle6',  99,     12,  13,   14, 15, 16,99,     12,  13,   14, 15, 16);"""
cursor.execute(sql)

sql = """INSERT INTO throughput(
         VehicleID, Vehicle0, Vehicle1, Vehicle2, Vehicle3, Vehicle4, Vehicle5, Vehicle6, Vehicle7, Vehicle8, Vehicle9, Vehicle10, Vehicle11)
         VALUES ('Vehicle7',  99,     12,  13,   14, 15, 16,99,     12,  13,   14, 15, 16);"""
cursor.execute(sql)

sql = """INSERT INTO throughput(
         VehicleID, Vehicle0, Vehicle1, Vehicle2, Vehicle3, Vehicle4, Vehicle5, Vehicle6, Vehicle7, Vehicle8, Vehicle9, Vehicle10, Vehicle11)
         VALUES ('Vehicle8',  99,     12,  13,   14, 15, 16,99,     12,  13,   14, 15, 16);"""
cursor.execute(sql)

sql = """INSERT INTO throughput(
         VehicleID, Vehicle0, Vehicle1, Vehicle2, Vehicle3, Vehicle4, Vehicle5, Vehicle6, Vehicle7, Vehicle8, Vehicle9, Vehicle10, Vehicle11)
         VALUES ('Vehicle9',  99,     12,  13,   14, 15, 16,99,     12,  13,   14, 15, 16);"""
cursor.execute(sql)

sql = """INSERT INTO throughput(
         VehicleID, Vehicle0, Vehicle1, Vehicle2, Vehicle3, Vehicle4, Vehicle5, Vehicle6, Vehicle7, Vehicle8, Vehicle9, Vehicle10, Vehicle11)
         VALUES ('Vehicle10',  99,     12,  13,   14, 15, 16,99,     12,  13,   14, 15, 16);"""
cursor.execute(sql)

sql = """INSERT INTO throughput(
         VehicleID, Vehicle0, Vehicle1, Vehicle2, Vehicle3, Vehicle4, Vehicle5, Vehicle6, Vehicle7, Vehicle8, Vehicle9, Vehicle10, Vehicle11)
         VALUES ('Vehicle11',  99,     12,  13,   14, 15, 16,99,     12,  13,   14, 15, 16);"""
cursor.execute(sql)
db.commit()

db.close()
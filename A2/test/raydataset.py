import sqlite3

conn = sqlite3.connect("/home/jaimin/ray_nfs/VEC.db")
cursor = conn.cursor()
sql = """select * from BASESTATION"""
cursor.execute(sql)
result = cursor.fetchall()
print(result)
print(type(result))
conn.close()

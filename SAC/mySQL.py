import pandas as pd
import pymysql
import numpy as np

mydb = pymysql.connect(
  host="localhost",
  user="zequn",
  password="666888",
  database="SAC"
)

# mycursor = mydb.cursor()

# mycursor.execute("SELECT offloading_delay FROM sacenv")

sqlcmd = "select offloading_delay from sacenv"

a = pd.read_sql(sqlcmd, mydb)

# myresult = mycursor.fetchall()

# myarray=np.array(myresult)
# for x in myresult:
x = np.array(a)
b = x(1)
print(b)


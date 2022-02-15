import math
import pandas as pd

def loc_cal(data: pd.DataFrame):
    z=0
    i=0
    for index, row in data.iterrows():
        # print(row[1])
        lg = float(row[0])
        cs = float(row[1])
        z += 3*math.log(lg) + math.cos(cs) ** 2
        i += 1
        if i>200 :
            break
    return z

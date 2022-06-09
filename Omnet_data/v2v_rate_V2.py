import pymysql
import numpy as np
import pandas as pd
import time
import udp_request
import struct
import random
''' 
-------------------------------------------------------------------------------------
|  vehicle ID  |  Vehicle 1 | Vehicle 2| Vehicle 3| ... |
|   Vehicle 1  |    .....   |    ..... |   .....  | ... |
...
--------------------------------------------------------------------------------------
'''
db0 = pymysql.connect(
     host = "192.168.1.117",
     user = "VEC",
     password = "666888",
     database = "SAC",
)

db1 = pymysql.connect(
     host = "192.168.1.122",
     user = "VEC",
     password = "666888",
     database = "SAC",
)


def update_throughput(throughput_data:pd.DataFrame, loop_count, cursor):
    # Update data into ts_vehicle
    event = str(1)
    input_list = []
    for node1 in range(12):
        sql = "UPDATE throughput SET Vehicle0 = %s, Vehicle1 = %s, Vehicle2 = %s, Vehicle3 = %s, Vehicle4 = %s, Vehicle5 = %s, Vehicle6 = %s, Vehicle7 = %s, " \
                + "Vehicle8 = %s, Vehicle9 = %s, Vehicle10 = %s, Vehicle11 = %s WHERE VehicleID='Vehicle" + str(node1) + "'"
        for node2 in range(12):
            if node2 > node1:
                specific_rate = "Node" + str(node1) + "-" + str(node2)
                input_list.append(throughput_data.loc[loop_count,specific_rate])
            elif node2 < node1:
                specific_rate = "Node" + str(node2) + "-" + str(node1)
                input_list.append(throughput_data.loc[loop_count,specific_rate])
            else:
                input_list.append(99.0)
        input_tuple = tuple(input_list)
        input_list.clear()
        cursor.execute(sql,input_tuple)

def update_uti(v0:list, v1:list, v2:list, v3:list, cursor):
    sql = "UPDATE vehicle_information SET Fs=%s, utilization=%s WHERE ID = %s"
    cursor.execute(sql,(str(v0[1]),str(v0[2]),str(v0[0])))
    cursor.execute(sql,(str(v1[1]),str(v1[2]),str(v1[0])))
    cursor.execute(sql,(str(v2[1]),str(v2[2]),str(v2[0])))
    cursor.execute(sql,(str(v3[1]),str(v3[2]),str(v3[0])))

# Update data
if __name__ == "__main__":
    loop_count = 1
    throughput_data = pd.read_csv("./throughput.csv",index_col="Time")
    IP_pool = []
    for i in range(12):
        add_IP="192.168.1.1"+str(60+i)
        IP_pool.append(add_IP)
    print(IP_pool)
    while 1:
        # ID, Fs, utilization

        # if loop_count == 5:
        #     # In this event, vehicles start just now and not crowded around BS
        #     # Task vehicle: vehicle0, others are service vehicles
        #     # Vehicle0,2,3 are busy (90%), vehicle1 is free (3%)
        #     # SAC result: choose vehicle1

        #     # all vehicles send requests to the BS[0]
        #     # DDQN result: BS[1]
        #     v0=[0, 7.0, 90]
        #     v1=[1, 6.5, 3.0]
        #     v2=[2, 5.5, 90]
        #     v3=[3, 6.3, 90]
        #     ts_id = "192.168.1.119"


        # elif loop_count == 30:
        #     # In this event, vehicles are all around BS[0]
        #     # Task vehicle: vehicle1, others are service vehicles
        #     # Vehicle0,1,3 are busy, vehicle2 is free
        #     # SAC result: choose vehicle2

        #     # all vehicles send requests to the BS[0]
        #     # DDQN result: BS[1]
        #     v0=[0, 7.0, 95]
        #     v1=[1, 6.5, 85]
        #     v2=[2, 5.5, 6.0]
        #     v3=[3, 6.3, 92]
        #     ts_id = "192.168.1.121"

        # elif loop_count == 65:
        #     # In this event, vehicles are all around BS[1]
        #     # Task vehicle: vehicle3, others are service vehicles
        #     # Vehicle0,2,3 are busy, vehicle1 is free
        #     # SAC result: choose vehicle1

        #     # all vehicles send requests to the BS[1]
        #     # DDQN result: BS[0]
        #     v0=[0, 7.0, 95]
        #     v1=[1, 6.5, 8]
        #     v2=[2, 5.5, 84]
        #     v3=[3, 6.3, 92]
        #     ts_id = "192.168.1.124"
        # else:
        v0=[0, 7.0, 5.0]
        v1=[1, 7, 5.0]
        v2=[2, 7, 5.0]
        v3=[3, 7, 5.0]
        ts_id = random.choice(IP_pool)
        
        if loop_count  > 4:
            bs_id= "1"
            db = db1
        else:
            bs_id= "0"
            db = db0
        

        cursor = db.cursor()
        # Update vehicla utlizaiton
        # update_uti(v0,v1,v2,v3,cursor)


        
        update_throughput(throughput_data,loop_count,cursor)
        # time delay
        db.commit()
        control_msg = struct.pack("!i10s10s",2,b"control",bs_id.encode())
        udp_request.control_send(control_msg,ts_id)
        print("Event:",loop_count,"Task vehicle is:",ts_id,"Choose base station ",bs_id)
        time.sleep(2)

        # print("Update Successfully")
        # increase loop_count
        if loop_count < 8:
            loop_count += 1
        else:
            loop_count = 1
    db.close()
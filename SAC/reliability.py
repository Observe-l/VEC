import os
import docker
import json
import time
from Para_def import SACEnv

client = docker.APIClient(base_url='unix:///var/run/docker.sock')
class vehicle():
    def __init__(self, id = 0, ra = 0, re = 0):
        self.id = id
        self.ra = ra
        self.re = re

def update(vehicle: vehicle):
    cmd = " peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel "\
                +"-n vehicle --tls --cafile /opt/gopath/src/github.com/hyperl"\
                +"edger/fabric/peer/crypto/ordererOrganizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem " \
                +"-c '{\"Args\":[\"set\",\"" + str(vehicle.id) + "\","\
                    + "\"" + str(vehicle.ra)+"\",\""+str(vehicle.re)+"\"]}'"
    # Create a docker command
    id1 = client.exec_create('cli1',cmd)

    # Execute the docker command
    result1 = client.exec_start(id1).decode()

def getByID(id: int):
    cmd = "peer chaincode query -C vec-channel -n vehicle "\
            + " -c '{\"Args\":[\"get\",\"" + str(id) + "\"]}' "
    # Create a docker command
    id1 = client.exec_create('cli1',cmd)

    # Execute the docker command
    result1 = client.exec_start(id1).decode()

    # Ledger will return a json format data, convert it to a python dict
    js_data = json.loads(result1)
    vehicle_get = vehicle(id=id)
    vehicle_get.ra=js_data['completion_ratio']
    vehicle_get.re=js_data['reliability']
    return vehicle_get

def delByID(id: int):
    cmd = " peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel "\
                +"-n vehicle --tls --cafile /opt/gopath/src/github.com/hyperle"\
                +"dger/fabric/peer/crypto/ordererOrganizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem" \
                +"-c '{\"Args \":[\"del\",\"" + str(id) + "\"]}'"

    # Create a docker command
    id1 = client.exec_create('cli1',cmd)
    # Execute the docker command
    result1 = client.exec_start(id1).decode()

def getAlldata(startkey="", endkey=""):
    cmd = "peer chaincode query -C vec-channel -n vehicle "\
            + " -c '{\"Args\":[\"bslist\",\""+startkey+"\",\""+endkey+"\"""]}'"
    id1 = client.exec_create('cli1',cmd)

    # Execute the docker command
    result1 = client.exec_start(id1).decode()

    # Ledger will return a json format data, convert it to a python dict
    js_data = json.loads(result1)

    # Create a list of Base station class
    if len(js_data)==0:
        return 0
    else:
        vs = [vehicle() for i in range(len(js_data))]
        for i in range(len(js_data)):
            vs[i].id = int(js_data[i]['Record']['id'])
            vs[i].ra = float(js_data[i]['Record']['completion_ratio'])
            vs[i].re = float(js_data[i]['Record']['reliability'])
    return vs

def mul_get(id:list):
    cmd = " peer chaincode query -C vec-channel -n vehicle "\
            + " -c '{\"Args\":[\"mul_get\""
    for i in id:
        cmd = cmd + ",\"" + str(i) + "\""
    cmd = cmd + "]}'"
    id1 = client.exec_create('cli1',cmd)

    # Execute the docker command
    result1 = client.exec_start(id1).decode()

    # Ledger will return a json format data, convert it to a python dict
    js_data = json.loads(result1)

    # Create a list of Base station class
    if len(js_data)==0:
        return 0
    else:
        vs = [vehicle() for i in range(len(js_data))]
        for i in range(len(js_data)):
            vs[i].id = js_data[i]['Record']['id']
            vs[i].ra = float(js_data[i]['Record']['completion_ratio'])
            vs[i].re = float(js_data[i]['Record']['reliability'])
    return vs

def mul_set(data:SACEnv):
    cmd = " peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel "\
                +"-n vehicle --tls --cafile /opt/gopath/src/github.com/hyperl"\
                +"edger/fabric/peer/crypto/ordererOrganizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem " \
                + " -c '{\"Args\":[\"mul_set\""
    for i in range(data.s):
        cmd = cmd + ",\"", + str(data.id[i]) + "\",\"" + str(data.completion_ratio[i]) \
                + "\",\"" + str(data.reliability[i]) + "\""
    cmd = cmd + "]}'"
    id1 = client.exec_create('cli1',cmd)
    result1 = client.exec_start(id1).decode()

if __name__ == '__main__':
    # all_data = getAlldata()
    up_data = vehicle(0,5.31,3.22)
    update(up_data)
    id_list = [1,3,2]
    all_data = mul_get(id_list)
    for i in range(len(all_data)):
        print("Data ",i," is:",all_data[i].id)
    # freememory()
    

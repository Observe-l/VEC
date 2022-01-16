import docker
import json
import time
from BaseStation import BaseStation

# Update/instert one data to ledger.
def update(bs: BaseStation):
    client = docker.APIClient(base_url='unix:///var/run/docker.sock')
    cmd = " peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel "\
                +"-n a2c --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem " \
                +"-c '{\"Args\":[\"set\",\"" + str(bs.id) + "\","\
                    + "\"" + str(bs.global_computing_resource) + "\","\
                    + "\"" + str(bs.reversed_computing_resource) + "\","\
                    + "\"" + str(bs.computing_efficiency) + "\","\
                    + "\"" + str(bs.completion_ratio) + "\","\
                    + "\"" + str(bs.total_received_task) + "\","\
                    + "\"" + str(bs.reliability) + "\"]}'"
    # Create a docker command
    id1 = client.exec_create('cli1',cmd)

    # Execute the docker command
    result1 = client.exec_start(id1).decode()

# Get one data from ledged. Recommde use mul_get function to get two or more data.
# This function will return a class
def getByID(id: str):
    client = docker.APIClient(base_url='unix:///var/run/docker.sock')
    cmd = " peer chaincode query -C vec-channel -n a2c "\
            + " -c '{\"Args\":[\"get\",\"" + id + "\"]}' "
    # Create a docker command
    id1 = client.exec_create('cli1',cmd)

    # Execute the docker command
    result1 = client.exec_start(id1).decode()

    # Ledger will return a json format data, convert it to a python dict
    js_data = json.loads(result1)
    bs = BaseStation()
    bs.id = js_data['id']
    bs.global_computing_resource = float(js_data['global_computing_resource'])
    bs.reversed_computing_resource = float(js_data['reversed_computing_resource'])
    bs.computing_efficiency = float(js_data['computing_efficiency'])
    bs.completion_ratio = float(js_data['completion_ratio'])
    bs.total_received_task = float(js_data['total_received_task'])
    bs.reliability = float(js_data['reliability'])
    return bs

# Get data by ID. Input variable should be a list of ID. 
# This function will return a list of Base station data (calss)
def mul_getByID(id: list):
    client = docker.APIClient(base_url='unix:///var/run/docker.sock')
    cmd = " peer chaincode query -C vec-channel -n a2c "\
            + " -c '{\"Args\":[\"mul_get\""
    length = len(id)
    for i in id:
        cmd = cmd + ",\"" + i + "\""
    cmd = cmd + "]}'"

    # Create a docker command
    id1 = client.exec_create('cli1',cmd)

    # Execute the docker command
    result1 = client.exec_start(id1).decode()

    # Ledger will return a json format data, convert it to a python dict
    js_data = json.loads(result1)

    # Create a list of Base station class
    bs = [BaseStation() for i in range(length)]
    for i in range(length):
        bs[i].id = js_data[i]['Record']['id']
        bs[i].global_computing_resource = float(js_data[i]['Record']['global_computing_resource'])
        bs[i].reversed_computing_resource = float(js_data[i]['Record']['reversed_computing_resource'])
        bs[i].computing_efficiency = float(js_data[i]['Record']['computing_efficiency'])
        bs[i].completion_ratio = float(js_data[i]['Record']['completion_ratio'])
        bs[i].total_received_task = float(js_data[i]['Record']['total_received_task'])
        bs[i].reliability = float(js_data[i]['Record']['reliability'])
    return bs

# Delete a Base Station data
def delByID(id: str):
    client = docker.APIClient(base_url='unix:///var/run/docker.sock')
    cmd = " peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel "\
                +"-n a2c --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem" \
                +"-c '{\"Args \":[\"del\",\"" + id + "\"]}'"

    # Create a docker command
    id1 = client.exec_create('cli1',cmd)

    # Execute the docker command
    result1 = client.exec_start(id1).decode()

if __name__ == '__main__':
    # Mul_get, bs is a list of Basestation
    id = ['bs-1','bs-2','bs-3']
    bs = mul_getByID(id)    
    print(bs[1].id)
    

    # Update
    bs2 = BaseStation()
    bs2.id = 'bs-3'
    bs2.global_computing_resource = 10.2
    bs2.reversed_computing_resource = 3.5
    bs2.computing_efficiency = 0
    bs2.completion_ratio = 0
    bs2.total_received_task = 0
    bs2.reliability = 0
    # update(bs2)


    # Get by ID
    # bs3 = getByID('bs-3')
    # print(bs3.reversed_computing_resource)
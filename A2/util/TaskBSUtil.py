import docker
import json
import time
from util.Task import Task

# Update/instert one data to ledger.
def update(task: Task):
    client = docker.APIClient(base_url='unix:///var/run/docker.sock')
    cmd = " peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel "\
                +"-n a2c --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem " \
                +"-c '{\"Args\":[\"set\",\"" + str(task.id) + "\","\
                    + "\"" + str(task.offload_vehicle_id) + "\","\
                    + "\"" + str(task.service_vehicle_id) + "\","\
                    + "\"" + str(task.allocation_basestation_id) + "\","\
                    + "\"" + str(task.done_status) + "\","\
                    + "\"" + str(task.vehicle_density) + "\","\
                    + "\"" + str(task.delay) + "\"]}'"
    # Create a docker command
    id1 = client.exec_create('cli1',cmd)

    # Execute the docker command
    result1 = client.exec_start(id1).decode()

def countAllByBS(basestation_id):
    pass


def countDoneByBS(basestation_id):
    pass



def selectLatest(num):
    pass

def countAll():
    pass
    

def getFirstId():
    pass
    

def getLastId():
    pass

def deleteAllTasks():
    pass


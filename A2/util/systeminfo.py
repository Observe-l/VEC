import os
import docker
import json
import time

from grpc import Status
from Task import Task
def freememory():
    cmd="free"
    stream = os.popen(cmd)
    f=stream.read().split(" ")
    f=list(f)
    s={}
    for i,v in enumerate(f):
        if v=="":
            pass
        else:
            s[i] = v
    # print("total_memory: "+str(s[49]))
    print("free memory: "+str(s[58]))
    return [s[48],s[58]]
class BS():
    def __init__(self,id=None, tm=None, fm=None):
        self.id = id
        self.tm = tm
        self.fm = fm
client = docker.APIClient(base_url='unix:///var/run/docker.sock')
def update(bs:BS):
    cmd = " peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel "\
                +"-n sacc --tls --cafile /opt/gopath/src/github.com/hyperl"\
                +"edger/fabric/peer/crypto/ordererOrganizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem " \
                +"-c '{\"Args\":[\"set\",\"" + str(bs.id) + "\","\
                    + "\"" + str(bs.tm)+"\",\""+str(bs.fm)+"\"]}'"
    # Create a docker command
    id1 = client.exec_create('cli1',cmd)

    # Execute the docker command
    result1 = client.exec_start(id1).decode()
    print("congratulations! the bs info has been added to the blockchain")
def getByID(id: str):
        cmd = "peer chaincode query -C vec-channel -n sacc "\
                + " -c '{\"Args\":[\"get\",\"" + id + "\"]}' "
        # Create a docker command
        id1 = client.exec_create('cli1',cmd)

        # Execute the docker command
        result1 = client.exec_start(id1).decode()

        # Ledger will return a json format data, convert it to a python dict
        js_data = json.loads(result1)
        bs = BS()
        bs.id = id
        bs.tm=js_data['total_memory']
        bs.fm=js_data['free_memory']
        return bs
def delByID(id: str):
        cmd = " peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel "\
                    +"-n sacc --tls --cafile /opt/gopath/src/github.com/hyperle"\
                    +"dger/fabric/peer/crypto/ordererOrganizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem" \
                    +"-c '{\"Args \":[\"del\",\"" + id + "\"]}'"

        # Create a docker command
        id1 = client.exec_create('cli1',cmd)
        # Execute the docker command
        result1 = client.exec_start(id1).decode()
        print("TaskID {} has been deleted".format(id))
def getAllTask(self, startkey="", endkey=""):
        cmd = "peer chaincode query -C vec-channel -n sacc "\
                + " -c '{\"Args\":[\"bslist\",\""+startkey+"\",\""+endkey+"\"""]}'"
        id1 = self.client.exec_create('cli1',cmd)

        # Execute the docker command
        result1 = self.client.exec_start(id1).decode()

        # Ledger will return a json format data, convert it to a python dict
        js_data = json.loads(result1)

        # Create a list of Base station class
        if len(js_data)==0:
            return 0
        else:
            bs = [BS() for i in range(len(js_data))]
            for i in range(len(js_data)):
                bs[i].id = js_data[i]['Record']['id']
                bs[i].tm = float(js_data[i]['Record']['total_memory'])
                bs[i].fm = float(js_data[i]['Record']['free_memory'])
        return bs
def autoupdate(bs:BS):
    while True:
        [tm,fm] = freememory()
        bs.id = "redPC"
        bs.tm = tm
        bs.fm = fm
        # delByID("redPC")
        update(bs)
        print(getByID("redPC").fm)
        time.sleep(5)
if __name__ == '__main__':
    bs=BS()
    autoupdate(bs)
    # freememory()
    

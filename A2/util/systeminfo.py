import os
import docker
import json
import time
import psutil
from grpc import Status
from Task import Task
class BSCPU():
        def __init__(self,id=None, cpu = None, tm=None, fm=None):
            self.id = id
            self.cpu=cpu
            self.tm = tm
            self.fm = fm
class systeminfo():

    def __init__(self):
        self.client = docker.APIClient(base_url='unix:///var/run/docker.sock')
    def cpuUtil(self,int_time:float):
        utl = psutil.cpu_percent(interval = int_time, percpu = False)
        print("average cpu utilization: ",utl)
        return utl
    def freememory(self):
        all_mem = psutil.virtual_memory()._asdict()
        total_mem = all_mem['total']
        free_mem = all_mem['available']
        print([total_mem, free_mem])
        return [total_mem, free_mem]
    
    
    def update(self,bs:BSCPU):
        cmd = " peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel "\
                    +"-n sacc --tls --cafile /opt/gopath/src/github.com/hyperl"\
                    +"edger/fabric/peer/crypto/ordererOrganizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem " \
                    +"-c '{\"Args\":[\"set\",\"" + str(bs.id) + "\","\
                        + "\""+str(bs.cpu)+"\",\""+str(bs.tm)+"\",\""+str(bs.fm)+"\"]}'"
        # Create a docker command
        id1 = self.client.exec_create('cli1',cmd)

        # Execute the docker command
        result1 = self.client.exec_start(id1).decode()
        print("congratulations! the bs info has been added to the blockchain")
    def getByID(self, id: str):
            cmd = "peer chaincode query -C vec-channel -n sacc "\
                    + " -c '{\"Args\":[\"get\",\"" + id + "\"]}' "
            # Create a docker command
            id1 = self.client.exec_create('cli1',cmd)

            # Execute the docker command
            result1 = self.client.exec_start(id1).decode()

            # Ledger will return a json format data, convert it to a python dict
            js_data = json.loads(result1)
            bs = BSCPU()
            bs.id = id
            bs.cpu = js_data['CPU_UTIL']
            bs.tm=js_data['total_memory']
            bs.fm=js_data['free_memory']
            return bs
    def delByID(self,id: str):
            cmd = " peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel "\
                        +"-n sacc --tls --cafile /opt/gopath/src/github.com/hyperle"\
                        +"dger/fabric/peer/crypto/ordererOrganizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem" \
                        +"-c '{\"Args \":[\"del\",\"" + id + "\"]}'"

            # Create a docker command
            id1 = self.client.exec_create('cli1',cmd)
            # Execute the docker command
            result1 = self.client.exec_start(id1).decode()
            print("TaskID {} has been deleted".format(id))
    def getAllTask(self,startkey="", endkey=""):
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
                bs = [BSCPU() for i in range(len(js_data))]
                for i in range(len(js_data)):
                    bs[i].id = js_data[i]['Record']['id']
                    bs[i].cpu=float(js_data[i]['Record']['CPU_UTIL'])
                    bs[i].tm = float(js_data[i]['Record']['total_memory'])
                    bs[i].fm = float(js_data[i]['Record']['free_memory'])
            return bs
    def autoupdate(self,bs:BSCPU):
        while True:
            [tm,fm] = self.freememory()
            bs.id = "redPC"
            bs.cpu = self.cpuUtil(5)
            bs.tm = tm
            bs.fm = fm
            # delByID("redPC")
            self.update(bs)
            print(self.getByID("redPC").cpu)
            time.sleep(5)
if __name__ == '__main__':
    systeminfo = systeminfo()
    bs=BSCPU()
    # cpuUtil(1.5)
    # freememory()
    systeminfo.autoupdate(bs)
    

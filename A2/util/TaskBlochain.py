import docker
import json
import time

from grpc import Status
from Task import Task
class taskBlockchain():
    def __init__(self):
        self.client = docker.APIClient(base_url='unix:///var/run/docker.sock')
    # Update/instert one data to ledger.
    def update(self,task: Task):
        cmd = " peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel "\
                    +"-n task --tls --cafile /opt/gopath/src/github.com/hyperl"\
                    +"edger/fabric/peer/crypto/ordererOrganizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem " \
                    +"-c '{\"Args\":[\"set\",\"" + str(task.id) + "\","\
                        + "\"" + str(task.offload_vehicle_id) + "\","\
                        + "\"" + str(task.service_vehicle_id) + "\","\
                        + "\"" + str(task.allocation_basestation_id) + "\","\
                        + "\"" + str(task.delay) + "\","\
                        + "\"" + str(task.done_status) + "\","\
                        + "\"" + str(task.vehicle_density) + "\"]}'"
        # Create a docker command
        id1 = self.client.exec_create('cli1',cmd)

        # Execute the docker command
        result1 = self.client.exec_start(id1).decode()
        print("congratulations! the task has been added to the blockchain")

    # Get one data from ledged. Recommde use mul_get function to get two or more data.
    # This function will return a class
    def getByID(self, id: str):
        cmd = " peer chaincode query -C vec-channel -n task "\
                + " -c '{\"Args\":[\"get\",\"" + id + "\"]}' "
        # Create a docker command
        id1 = self.client.exec_create('cli1',cmd)

        # Execute the docker command
        result1 = self.client.exec_start(id1).decode()

        # Ledger will return a json format data, convert it to a python dict
        js_data = json.loads(result1)
        task = Task()
        task.id = js_data['id']
        task.offload_vehicle_id = float(js_data['offload_vehicle_id'])
        task.service_vehicle_id = float(js_data['service_vehicle_id'])
        task.allocation_basestation_id = float(js_data['allocation_basestation_id'])
        task.delay = float(js_data['delay'])
        task.done_status = float(js_data['done_status'])
        task.vehicle_density = js_data['vehicle_density']
        return task

    # Get data by ID. Input variable should be a list of ID. 
    # This function will return a list of Base station data (calss)
    def mul_getByID(self, id: list):
        cmd = " peer chaincode query -C vec-channel -n task "\
                + " -c '{\"Args\":[\"mul_get\""
        length = len(id)
        for i in id:
            cmd = cmd + ",\"" + i + "\""
        cmd = cmd + "]}'"

        # Create a docker command
        id1 = self.client.exec_create('cli1',cmd)

        # Execute the docker command
        result1 = self.client.exec_start(id1).decode()

        # Ledger will return a json format data, convert it to a python dict
        js_data = json.loads(result1)

        # Create a list of Base station class
        task = [Task() for i in range(length)]
        for i in range(length):
            task[i].id = js_data[i]['Record']['id']
            task[i].offload_vehicle_id = float(js_data[i]['Record']['offload_vehicle_id'])
            task[i].service_vehicle_id = float(js_data[i]['Record']['service_vehicle_id'])
            task[i].allocation_basestation_id = float(js_data[i]['Record']['allocation_basestation_id'])
            task[i].delay = float(js_data[i]['Record']['delay'])
            task[i].done_status = float(js_data[i]['Record']['done_status'])
            task[i].vehicle_density = js_data[i]['Record']['vehicle_density']
        return task

    # Delete a Base Station data
    def delByID(self, id: str):
        cmd = " peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel "\
                    +"-n task --tls --cafile /opt/gopath/src/github.com/hyperle"\
                    +"dger/fabric/peer/crypto/ordererOrganizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem" \
                    +"-c '{\"Args \":[\"del\",\"" + id + "\"]}'"

        # Create a docker command
        id1 = self.client.exec_create('cli1',cmd)
        # Execute the docker command
        result1 = self.client.exec_start(id1).decode()
        print("TaskID {} has been deleted".format(id))
    def getAllTask(self):
        cmd = "peer chaincode query -C vec-channel -n task -c '{\"Args\":[\"bslist\"]}'"
        id1 = self.client.exec_create('cli1',cmd)

        # Execute the docker command
        result1 = self.client.exec_start(id1).decode()

        # Ledger will return a json format data, convert it to a python dict
        js_data = json.loads(result1)

        # Create a list of Base station class
        if len(js_data)==0:
            return 0
        else:
            task = [Task() for i in range(len(js_data))]
            for i in range(len(js_data)):
                task[i].id = js_data[i]['Record']['id']
                task[i].offload_vehicle_id = float(js_data[i]['Record']['offload_vehicle_id'])
                task[i].service_vehicle_id = float(js_data[i]['Record']['service_vehicle_id'])
                task[i].allocation_basestation_id = float(js_data[i]['Record']['allocation_basestation_id'])
                task[i].delay = float(js_data[i]['Record']['delay'])
                task[i].done_status = float(js_data[i]['Record']['done_status'])
                task[i].vehicle_density = js_data[i]['Record']['vehicle_density']
        return task
    def delAllTask(self):
        if self.getAllTask()==0:
            print("Sadly! There is no task to delete")
        else:
            cmd = "peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel -n task --tls" \
                +" --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrga"\
                +"nizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem -c '{\"Args\":[\"delall\"]}'"
            id1 = self.client.exec_create('cli1',cmd)
            # Execute the docker command
            result1 = self.client.exec_start(id1).decode()
            print("All the Tasks are deleted")

if __name__ == '__main__':
    bchain=taskBlockchain()
    list = bchain.getAllTask()
    # task=Task()
    # task.id="123"
    # task.offload_vehicle_id = 567
    # task.service_vehicle_id = 9877
    # task.allocation_basestation_id = 2
    # task.done_status = 1
    # task.vehicle_density = "{2:3, 1:2}"
    # task.delay = 5
    # bchain.update(task)
    # bchain.delByID("123")
    # bchain.delAllTask()
    # tasklist=bchain.getAllTask()
    # print(tasklist[0].id)
    # print(tasklist[0].offload_vehicle_id)
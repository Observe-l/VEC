import docker
import time
import json

client = docker.APIClient(base_url='unix:///var/run/docker.sock')

cmd1 = ''' peer chaincode query -C vec-channel -n sacc -c '{"Args":["query","tv-2"]}' '''
cmd2 = ''' peer chaincode query -C vec-channel -n a2c -c '{"Args":["query","bs-2"]}' '''
cmd3 = ''' peer chaincode query -C vec-channel -n sacc -c '{"Args":["mul_get","tv-1","tv-2","tv-3","tv-4","tv-5","tv-6","tv-7","tv-8"]}' '''
cmd4 = ''' peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel -n sacc --tls 
            --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem 
            -c '{"Args":["set","tv-2","10"]}' '''
cmd5 = ''' peer chaincode query -C vec-channel -n a2c -c '{"Args":["mul_get","bs-1","bs-2"]}' '''
start_time = time.time()
id1 = client.exec_create('cli1',cmd1)
id2 = client.exec_create('cli1',cmd2)
id3 = client.exec_create('cli1',cmd3)
id4 = client.exec_create('cli1',cmd4)
id5 = client.exec_create('cli1',cmd5)
# result1 = float(client.exec_start(id1).decode())
# result2 = float(client.exec_start(id2).decode())
# result3 = client.exec_start(id3).decode()
result4 = client.exec_start(id5).decode()
end_time = time.time()
cov_data = json.loads(result4)
typeof=type(cov_data[0]['Record']['global_computing_resource'])
print("result:\n",cov_data[0]['Record'])
print(typeof)
print("Total time is:",end_time-start_time)

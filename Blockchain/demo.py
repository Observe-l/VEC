import docker
import time

client = docker.APIClient(base_url='unix:///var/run/docker.sock')

cmd1 = ''' peer chaincode query -C vec-channel -n sacc -c '{"Args":["query","tv-2"]}' '''
cmd2 = ''' peer chaincode query -C vec-channel -n sacc -c '{"Args":["query","tv-3"]}' '''
cmd3 = ''' peer chaincode query -C vec-channel -n sacc -c '{"Args":["mul_get","tv-1","tv-2","tv-3","tv-4","tv-5","tv-6","tv-7","tv-8"]}' '''
id1 = client.exec_create('cli1',cmd1)
id2 = client.exec_create('cli1',cmd2)
id3 = client.exec_create('cli1',cmd3)
# result1 = float(client.exec_start(id1).decode())
# result2 = float(client.exec_start(id2).decode())
result3 = client.exec_start(id3).decode()
print("result:",result3)

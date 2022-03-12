import docker
import csv
client = docker.APIClient(base_url='unix:///var/run/docker.sock')
# cmd = "sawtooth keygen bs1 --force"
# id1=client.exec_create('simplewallet-client-1',cmd)
# output=client.exec_start(id1).decode().strip()
# print(output)
cmd = "simplewallet deposit '140 20 30 40 60 80' bs1"
id1=client.exec_create('simplewallet-client-1',cmd)
client.exec_start(id1)
cmd = "simplewallet balance bs1"
id1=client.exec_create('simplewallet-client-2',cmd)
data = client.exec_start(id1).decode().strip()
print(data)
# result={}
# columns=["global_computing_resource", "reserved_resource","comp_eff","completion_ratio","total_task","reliability"]
# for i in range(len(data)):
#     result[columns[i]]=data[i]
# print(result)
# with open('C:\\Users\\Arunava\\Desktop\\sawtooth-simplewallet\\pyclient\\dct.csv', 'w') as f:
#     writer = csv.writer(f)
#     for k, v in result.items():
#        writer.writerow([k, v])

# cmd = "sawtooth settings list --url tcp://validator-1:8008"
# id1=client.exec_create('validator-0',cmd)
# data = client.exec_start(id1).decode().strip()
# print(data)
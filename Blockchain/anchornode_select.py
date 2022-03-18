import docker
import string
import time

def anchornode_selection(node):
    t0 = time.clock()
    client=docker.APIClient(base_url='unix:///var/run/docker.sock')
    cmd="mkdir channel-artifacts1"
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()

    cmd="peer channel fetch config channel-artifacts1/config_block.pb "\
        +"-o orderer.gcp.com:7050 -c vec-channel --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/" \
            +"ordererOrganizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem"
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()

    cmd="configtxlator proto_decode --input channel-artifacts1/config_block.pb" \
        +" --type common.Block --output channel-artifacts1/config_block.json"
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()
    cmd="/bin/bash -c \"jq '.data.data[0].payload.data.config' channel-artifacts1/config_block.json > channel-artifacts1/config.json\""
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()
    # print(result)

    cmd="cp channel-artifacts1/config.json channel-artifacts1/config_copy.json"
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()

    cmd="jq '.channel_group.groups.Application.groups.RayMSP.values += "\
        +"{\"AnchorPeers\":{\"mod_policy\": \"Admins\",\"value\":{\"anchor_peers\": "\
        +"[{\"host\": \""+str(node)+"\",\"port\": 7051}]},\"version\": \"0\"}}' "\
        +"channel-artifacts1/config_copy.json"
    # print(cmd)
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()
    # print(result)

    result=result.replace("\"","\\\"")
    cmd="/bin/bash -c \'echo \""+str(result)+"\" > channel-artifacts1/modified_config.json\'"
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()
    # print(result)

    cmd="configtxlator proto_encode --input channel-artifacts1/config.json --type "\
        +"common.Config --output channel-artifacts1/config.pb"
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()
    cmd="configtxlator proto_encode --input channel-artifacts1/modified_config.json --type common.Config "\
        +"--output channel-artifacts1/modified_config.pb"
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()
    cmd="configtxlator compute_update --channel_id vec-channel "\
        +"--original channel-artifacts1/config.pb --updated channel-artifacts1/modified_config.pb --output channel-artifacts1/config_update.pb"
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()
    cmd="configtxlator proto_decode --input channel-artifacts1/config_update.pb --type common.ConfigUpdate"\
        +" --output channel-artifacts1/config_update.json"
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()

    cmd = "cat channel-artifacts1/config_update.json"
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()
    # print(result)



    cmd="echo '{\"payload\":{\"header\":{\"channel_header\":{\"channel_id\":\"vec-channel\", "\
        +"\"type\":2} },\"data\":{\"config_update\":" + str(result)+"}}}'"
    # print(cmd)
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode().translate({ord(c):None for c in string.whitespace})
    result=result.replace("\"","\\\"")
    # print(result)

    cmd="/bin/bash -c \'echo \""+str(result)+"\" > channel-artifacts1/test.json\'"
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()
    # print(result)

    cmd="/bin/bash -c \'jq . channel-artifacts1/test.json > channel-artifacts1/config_update_in_envelope.json\'"
    # print(cmd)
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()
    # print(result)
    
    cmd="configtxlator proto_encode --input channel-artifacts1/config_update_in_envelope.json "\
        +"--type common.Envelope --output channel-artifacts1/config_update_in_envelope.pb"
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()

    cmd="peer channel update -f channel-artifacts1/config_update_in_envelope.pb "\
        +"-c vec-channel -o orderer.gcp.com:7050 --tls --cafile \"/opt/gopath/src/"\
        +"github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/gcp.com/msp/tlscacerts/tlsca.gcp.com-cert.pem\""
    output=client.exec_create('cli1',cmd)
    result=client.exec_start(output).decode()
    t1=time.clock()-t0
    return t1

if __name__ == '__main__':
    b_id =0
    if b_id==0:
        print("time: {}".format(anchornode_selection("peer0.ray.com")))
    elif b_id==2:
        print("time: {}".format(anchornode_selection("peer1.ray.com")))
    elif b_id==3:
        print("time: {}".format(anchornode_selection("peer2.ray.com")))
    else:
        print("time: {}".format(anchornode_selection("peer4.ray.com")))

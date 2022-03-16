```shell
peer lifecycle chaincode package task.tar.gz --path /opt/gopath/src/github.com/hyperledger/fabric-cluster/chaincode/go/task --label task_27
peer lifecycle chaincode install task.tar.gz


peer lifecycle chaincode approveformyorg  -o orderer.gcp.com:7050 --channelID vec-channel --name task --version 1.0 --init-required --package-id task_14:05f582de06c0d5b7d6d5b1b494c059edced59c16b3affe668f7f4f16cf5c0173 --sequence 27 --tls --cafile "$ORDERER_CA"

peer lifecycle chaincode checkcommitreadiness -o orderer.gcp.com:7050 --channelID vec-channel --name task --version 1.0 --init-required --sequence 27 --tls --cafile "$ORDERER_CA"

peer lifecycle chaincode commit -o orderer.gcp.com:7050 --channelID vec-channel --name task --version 1.0 --sequence 27 --init-required --tls --cafile "$ORDERER_CA"


peer chaincode query -C vec-channel -n task -c '{"Args":["bslist"]}'

peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel -n task --tls --cafile "$ORDERER_CA" -c '{"Args":["delall"]}'

```


## Tools and client

[Hyperledger Fabric](https://hyperledger-fabric.readthedocs.io/en/latest/whatis.html)

### Create CA, MSP and some doc

```shell
cryptogen generate --config=cryptogen.yaml
```

### Create and join new channel

First, generate genesis block file and channel file at local directory

```shell
# Generate genesis block
configtxgen -outputBlock ./channel-artifacts/genesis.block -profile vecOrderGenesis -channelID mychannel
# Generate channel creation file
configtxgen -outputCreateChannelTx ./channel-artifacts/channel.tx -profile vecChannel -channelID vec-channel
```

​	The, start the docker compose, and create channel

```shell
# Create channel in cli
peer channel create -c vec-channel -f ./channel-artifacts/channel.tx --orderer orderer.gcp.com:7050 --tls true --cafile "$ORDERER_CA"
# Join in the channel in other machine
peer channel join -b vec-channel.block
```

**Set anchor peers**

```shell
# fetch the channel configuration:
peer channel fetch config channel-artifacts/config_block.pb -o orderer.gcp.com:7050 -c vec-channel --tls --cafile "$ORDERER_CA"

# In config folder, Decode the block from protobuf into a JSON object
cd channel-artifacts/

configtxlator proto_decode --input config_block.pb --type common.Block --output config_block.json
jq '.data.data[0].payload.data.config' config_block.json > config.json

# Add the Org1 anchor peer to the channel configuration.
cp config.json config_copy.json

jq '.channel_group.groups.Application.groups.RayMSP.values += {"AnchorPeers":{"mod_policy": "Admins","value":{"anchor_peers": [{"host": "peer0.ray.com","port": 7051}]},"version": "0"}}' config_copy.json > modified_config.json

# Convert configure file back into protobuf format and compare
configtxlator proto_encode --input config.json --type common.Config --output config.pb
configtxlator proto_encode --input modified_config.json --type common.Config --output modified_config.pb
configtxlator compute_update --channel_id vec-channel --original config.pb --updated modified_config.pb --output config_update.pb

# Wrap the configuration update in a transaction envelope
configtxlator proto_decode --input config_update.pb --type common.ConfigUpdate --output config_update.json
echo '{"payload":{"header":{"channel_header":{"channel_id":"vec-channel", "type":2}},"data":{"config_update":'$(cat config_update.json)'}}}' | jq . > config_update_in_envelope.json
configtxlator proto_encode --input config_update_in_envelope.json --type common.Envelope --output config_update_in_envelope.pb

# Ues "peer channel update" to add the anchor peer
cd ..

peer channel update -f channel-artifacts/config_update_in_envelope.pb -c vec-channel -o orderer.gcp.com:7050 --tls --cafile "$ORDERER_CA"
```



### Chain code lifestyle (on channel)

```shell
# Packet
peer lifecycle chaincode package sacc.tar.gz --path /opt/gopath/src/github.com/hyperledger/fabric-cluster/chaincode/go --label sacc_1
# Install go mod and vendor
go mod init
go mod vendor
# Install chaincode
peer lifecycle chaincode install sacc.tar.gz
# Approve the chaincode
peer lifecycle chaincode approveformyorg  -o orderer.gcp.com:7050 --channelID vec-channel --name sacc --version 1.0 --init-required --package-id sacc_1:78420af78f11182408ec7e99387eff4f6981a3f93565e56a65d6e3a86fbe63cf --sequence 1 --tls --cafile "$ORDERER_CA"

# Check status
peer lifecycle chaincode checkcommitreadiness -o orderer.gcp.com:7050 --channelID vec-channel --name sacc --version 1.0 --init-required --sequence 1 --tls --cafile "$ORDERER_CA"

# Commit chaincode
peer lifecycle chaincode commit -o orderer.gcp.com:7050 --channelID vec-channel --name sacc --version 1.0 --sequence 1 --init-required --tls --cafile "$ORDERER_CA"
```

### Use chain code

```shell
# Init
peer chaincode invoke -o orderer.gcp.com:7050 --isInit -C vec-channel -n sacc --tls --cafile "$ORDERER_CA" -c '{"Args":["tv-1","0.5"]}'

# Set
peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel -n sacc --tls --cafile "$ORDERER_CA" -c '{"Args":["set","tv-2","0.3"]}'

# Delete
peer chaincode invoke -o orderer.gcp.com:7050 -C vec-channel -n sacc --tls --cafile "$ORDERER_CA" -c '{"Args":["del","tv-1"]}'

# Search
peer chaincode query -C vec-channel -n sacc -c '{"Args":["get","tv-2"]}'

# Multiple search
peer chaincode query -C vec-channel -n sacc -c '{"Args":["mul_get","tv-1","tv-2","tv-3","tv-4","tv-5","tv-6","tv-7","tv-8"]}'

```

### Join a new exist channel

```shell
peer channel fetch oldest vec-channel.block -c vec-channel --orderer orderer.gcp.com:7050 --tls --cafile "$ORDERER_CA"
```






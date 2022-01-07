VEC-Blockchain



### Some important ray command

```shell
ray start --head --resources='{"Vehicle-1": 6}'
sudo mount -t nfs 192.168.31.196:/home/lwh/nfsroot /home/ubuntu/nfsroot -o nolock
sudo mount -t nfs 34.92.132.215:/home/lwh/ray_nfs ~/ray_nfs/ -o nolock
```

Http server

```shell
python -m http.server
httpweet
```

Blockchain

```shell
besu --data-path=data --genesis-file=../genesis.json --rpc-http-enabled --rpc-http-api=ETH,NET,IBFT --host-allowlist="*" --rpc-http-cors-origins="all"

besu --data-path=data --genesis-file=../genesis.json --bootnodes=enode://541eb02a581d0de15b6922d93d8bee57fdf2c1d8e85d1da8f5411f48fc7639f1053e97b3d524075575a9e502e22c274d9accd68b73af9d9528d1b13211a6b703@34.92.132.215:30303 --rpc-http-enabled --rpc-http-api=ETH,NET,IBFT --host-allowlist="*" --rpc-http-cors-origins="all"
```




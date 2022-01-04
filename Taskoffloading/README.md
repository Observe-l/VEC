VEC-Blockchain



### Some important ray command

```shell
ray start --head --resources='{"Vehicle-1": 6}'
ray start --address='192.168.31.196:6379' --redis-password='5241590000000000' --resources='{"Task-vehicle": 4}'
ray start --head --num-cpus=8 --num-gpus=1
a1 = Counter.options(num_cpus=1, resources={"Custom1": 1}).remote()
sudo mount -t nfs [2406:3003:206b:1265:ce96:f3cb:dc12:43d1]:/home/lwh/nfsroot /home/ubuntu/nfsroot -o nolock
sudo mount -t nfs 192.168.31.196:/home/lwh/nfsroot /home/ubuntu/nfsroot -o nolock
sudo mount -t nfs 34.92.132.215:/home/lwh/ray_nfs ~/ray_nfs/ -o nolock
sudo mount -t nfs 34.146.128.46:/home/arunava/ray_nfs ~/ray_nfs -o nolock
sudo nethogs
```

Http server

```shell
python -m http.server 8001
httpweet
```

Blockchain

```shell
besu --data-path=data --genesis-file=../genesis.json --rpc-http-enabled --rpc-http-api=ETH,NET,IBFT --host-allowlist="*" --rpc-http-cors-origins="all"

besu --data-path=data --genesis-file=../genesis.json --bootnodes=enode://541eb02a581d0de15b6922d93d8bee57fdf2c1d8e85d1da8f5411f48fc7639f1053e97b3d524075575a9e502e22c274d9accd68b73af9d9528d1b13211a6b703@34.92.132.215:30303 --rpc-http-enabled --rpc-http-api=ETH,NET,IBFT --host-allowlist="*" --rpc-http-cors-origins="all"
```




VEC-Blockchain



### Some important ray command

```shell
ray start --head --resources='{"vehicle1": 4}'
ray start --address='192.168.1.119:6379' --redis-password='5241590000000000' --resources='{"vehicle2": 4}'
sudo mount -t nfs 192.168.31.196:/home/lwh/nfsroot /home/ubuntu/nfsroot -o nolock
sudo mount -t nfs 34.92.132.215:/home/lwh/ray_nfs ~/ray_nfs/ -o nolock
```

### Http server

```shell
python -m http.server
httpweet
```



### Request Packet

| Type               | Head     | Data 1     | Data 2   | Data 3 |
| ------------------ | -------- | ---------- | -------- | ------ |
| offloading request | request  | vehicle ID | Event ID | Dn     |
| Complete task      | complete | Cn         | Cn/fn    | fn     |

### Action Packet

| Type          | Head       | Data 1        | Data 2    | Data 3    |
| ------------- | ---------- | ------------- | --------- | --------- |
| Allocate task | offloading | vehicle ID/IP | File name | Task name |
| Skip self     | skip       | none          | none      | none      |


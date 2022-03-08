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





### Application layer transmit protocol

|      | Packet length | Request         | Packet 1        | Packet 2       |
| ---- | ------------- | --------------- | --------------- | -------------- |
| type | int, 4 bits   | string, 10 bits | string, 10 bits | string, 10bits |

**ACK**: after receive the request/action packet

**Retransmit**: ACK should return in 0.1s, otherwise client will resent the request/action. (Maximum retransmit 2 times)

### Packet from Vehicle

| Type               | length    | Head     | Data 1      | Data 2             | Data 3            | Data 4 | Data 5   |
| ------------------ | --------- | -------- | ----------- | ------------------ | ----------------- | ------ | -------- |
| offloading request | 6 packets | request  | vehicle ID  | Event ID           | $D_n$             | $C_n$  | $\tau_n$ |
| Complete task      | 4 packets | complete | vehicle ID  | $C_n/f_n+\theta_n$ | successful / fail | -      | -        |
| Update state       | 4 packets | update   | vehicle ID  | $F_s$              | $l_s$             | -      | -        |
| ACK                | 2 packets | ACK      | action type | -                  | -                 | -      | -        |

### Packet from base station

| Type          | length    | Head       | Data 1       | Data 2 | Data 3 |
| ------------- | --------- | ---------- | ------------ | ------ | ------ |
| Allocate task | 2 packets | offloading | vehicle ID   | -      | -      |
| ACK           | 2 packet2 | ACK        | request type | -      | -      |


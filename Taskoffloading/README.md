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



### Computation Size

| file  | iteration times | total time | Max number |
| ----- | --------------- | ---------- | ---------- |
| 200 K | 1               | 0.02 s     | 180        |
| 200 K | 15              | 0.1 s      |            |
| 200 K | 30              | 0.2 s      |            |
| 1 M   | 1               | 0.04 s     | 36         |
| 1 M   | 15              | 0.5 s      |            |
| 1 M   | 30              | 1 s        |            |
| 2 M   | 1               | 0.075 s    | 18         |
| 2 M   | 10              | 0.62 s     |            |
| 2 M   | 20              | 1.3 s      |            |
| 3 M   | 1               | 0.1 s      | 13         |
| 3 M   | 10              | 0.84 s     |            |
| 3 M   | 15              | 1.4 s      |            |
| 4 M   | 1               | 0.125 s    | 11         |
| 4 M   | 10              | 1.1 s      |            |
| 4 M   | 15              | 1.55 s     |            |

 $F_s=[3,7],\,Dn=[0.14,3.6]$, Total time: $0.02 \thicksim 1.2$

RPi generate some task based on $F_s=7,\,T=0.2\thicksim0.514 \,s$. We can set different $F_s$ and utilization on base station, The available computing resource can be expressed as:  $f_s=random(3,7)*utilization$, in RPi program, $C_n$ is: $C_n=C_n(based\;on\;7GHz)*f_s/7GHz$, latest iteration times is: $iter=7/f_s*iter_{base}$



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

| Type          | length    | Head       | Data 1       | Data 2                  | Data 3 |
| ------------- | --------- | ---------- | ------------ | ----------------------- | ------ |
| Allocate task | 3 packets | offloading | vehicle ID   | $F_s$ (service vehicle) | -      |
| ACK           | 2 packet2 | ACK        | request type | -                       | -      |


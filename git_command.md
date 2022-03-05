### Use SSH to connect to Lab

1. Start NUS VPN
2. IP table:

| Machine   | System version | User name | Password  | NUS IP         | Lab IP        |
| --------- | -------------- | --------- | --------- | -------------- | ------------- |
| Laptop 1  | Ubuntu 16.04   | vec       | 666888    | 172.27.94.31   | 192.168.1.122 |
| Laptop 2  | Ubuntu 16.04   | vec       | 666888    | 172.27.84.136  | 192.168.1.125 |
| Blue PC 1 | Ubuntu 16.04   | vec       | 666888    | 172.27.104.197 | -             |
| Red PC    | Ubuntu 20.04   | vec       | 666888    | -              | 192.168.1.117 |
| RPi 1     | Ubuntu 20.04   | ubuntu    | raspberry | -              | 192.168.1.119 |
| RPi 2     | Ubuntu 20.04   | ubuntu    | raspberry | -              | 192.168.1.121 |
| RPi 3     | Ubuntu 20.04   | ubuntu    | raspberry | -              | 192.168.1.124 |

3. SSH

```shell
# Connect to laptop 1
$ ssh vec@172.27.94.31

# Connect to laptop 2
$ ssh vec@172.27.84.136

# Connect to blue PC
$ ssh vec@172.27.104.197
```

### Git command

**Download the code**

```shell
$ git clone git@github.com:Observe-l/VEC.git
```

**Update to latest version** (No local changes)

``` shell
$ git pull --rebase
```


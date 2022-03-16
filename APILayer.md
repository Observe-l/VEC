Blockchain Layer:

```shell
columns:
ID                                          string  `json:"id"`
OFFLOAD_VEHICLE_ID                          float64 `json:"offload_vehicle_id"`
SERVICE_VEHICLE_ID                          float64 `json:"service_vehicle_id"`
ALLOCATION_BASESTATION_ID                   float64 `json:"allocation_basestation_id"`
DELAY                                       float64 `json:"delay"`
DONE_STATUS                                 float64 `json:"done_status"`
VEHICLE_DENSITY                             string  `json:"vehicle_density"`

Operations Type:
Query: to read the output for example fetch all the data from blockchain
Invoke: for write operation for example delete, set values

Operations:
set ---> the values one by one
del ----> deleted specific task 
get ----> fetch specific task
QueryAllBSs --->fetch all the tasks without any argument or with some specific range
delAllBSs ------> delete all existing task available in the blockchain or with some specific range
mul_get -----> fetch maultiple specific task
```

Application Layer:

```shell
API Name: taskBlockchain

Operations:
update  -----> set and update the tasks on blockchain via set function of Blockchain layer
getByID -----> fetch specific task via get function of Blockchain layer
mul_getByID -> fetch specific tasks via mul_get function of Blockchain layer
delByID -----> delete specific task via del function of Blockchain layer
getAllTask --> fetch all tasks with or without a range from blockchain via QueryAllBSs
delAllTask --> delete all the tasks with or without a range from blockchain via delAllBSs
```

DDQN Layer:

```shell
API Name: taskInteraction

Operations:
insert                              ----> update function of Application Layer
countAllByBS						----> getAllTask
CountDoneByBS						----> getAllTask
getNowTimeStamp	
selectLatest						----> getAllTask
countAll							----> getAllTask
getFirstId							----> getAllTask
getLastId							----> getAllTask
deleteAllTasks   					----> delAllTask
```




from util.Task import Task
import datetime
import json


def TaskDF2Task(taskDF):
    """transfer dataframe into basestation
    input: dataframe type
    output:basestation list type
    """

    taskValues = taskDF.values
    tasks = []
    for row in taskValues:
        task = Task()
        task.id = row[0]
        task.allocation_basestation_id=row[1]
        task.offload_vehicle_id=row[2]
        task.service_vehicle_id = row[3]
        task.delay= row[4]
        task.done_status=row[5]
        task.vehicle_density = json.loads(row[6])
        tasks.append(task)
    return tasks
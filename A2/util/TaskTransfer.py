from A2.util.Task import Task
import datetime
import json


def TaskDF2Task(taskDF):
    """transfer dataframe into basestation
    input: dataframe type
    output:basestation list type
    """
    dateformat = "%Y-%m-%d %H:%M:%S"
    taskValues = taskDF.values
    tasks = []
    for row in taskValues:
        task = Task()
        task.id = row[0]
        task.allocation_basestation_id=row[1]
        task.offload_vehicle_id=row[2]
        task.service_vehicle_id = row[3]
        # task.allocation_begin_time = datetime.datetime.strptime(row[4],dateformat)
        task.allocation_begin_time = row[4]
        # task.allocation_end_time = datetime.datetime.strptime(row[5],dateformat)
        task.allocation_end_time = row[5]
        diff=task.allocation_end_time-task.allocation_begin_time
        task.delay=diff.microseconds
        task.done_status=row[6]
        task.vehicle_density = json.loads(row[7])
        tasks.append(task)
    return tasks
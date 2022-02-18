from A2.util.Task import Task


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
        task.offload_vehicle_id= row[1]
        task.service_vehicle_id=row[2]
        task.allocation_basestation_id=row[3]
        task.allocation_begin_time=row[4]
        task.allocation_end_time=row[5]
        task.done_status=row[6]
        tasks.append(task)
    return tasks
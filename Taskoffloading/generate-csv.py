import csv

with open('Taskfile/task_4M.csv','a') as f:
    writer = csv.writer(f)
    data = ["log","cos","times"]
    writer.writerow(data)
    for i in range(1,250000):
        data = [i,i,1]
        writer.writerow(data)
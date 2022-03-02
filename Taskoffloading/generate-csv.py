import csv

with open('Taskfile/task_200Kbits.csv','w+') as f:
    writer = csv.writer(f)
    data = ["log","cos","times"]
    writer.writerow(data)
    for i in range(1,2100):
        data = [i,i,1]
        writer.writerow(data)
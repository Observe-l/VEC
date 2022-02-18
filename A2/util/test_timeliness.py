from TaskSQLUtil import countAllByBS
import time

if __name__ == '__main__':
    task_num = 0
    while True:
        time.sleep(2)
        temp_task_num = countAllByBS(1)
        temp_task_num += countAllByBS(2)
        if temp_task_num != task_num:
            task_num = temp_task_num
            print("insert one row!")
            break
    print("Go on!")

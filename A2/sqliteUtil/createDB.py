import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect('/home/jaimin/VEC.db')
    print('open database test.db successfully')
    c = conn.cursor()
    c.execute('''CREATE TABLE BASESTATION
    (id INT PRIMARY KEY NOT NULL,
     global_computing_resource REAL,
     reversed_computing_resource REAL,
     computing_efficiency REAL,
     completion_ratio REAL,
     total_received_task INT,
     reliability REAL
    );''')
    print('table create successfully')

    conn.commit()
    conn.close()









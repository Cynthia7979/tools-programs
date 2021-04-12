import os
import sqlite3

# os.chdir('E:\QQFileRecv')

conn = sqlite3.connect('./output.db')
cur = conn.cursor()
for table in cur.execute('SELECT name from sqlite_master where type= "table"'):
    print(table)
# for row in cur.execute(f'SELECT * from SIMPLE'):
#     print(row)
print('\n'.join([str(r) for r in cur.execute('SELECT * from SIMPLE').fetchall()[:5]]))
print(cur.execute('select * from MASTER').fetchall())
print(list(map(lambda x: x[0], cur.description)))
# print('\n'.join([str(r) for r in cur.execute('SELECT * from sqlite_sequence')]))


conn.close()
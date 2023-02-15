import pandas as pd
from mysql.connector import (connection)
from important_data import *

# 1. csv 파일 읽고 data 추가 
df_customer = pd.read_csv('./2023.02/02.14.d93_team_study/customer.csv', sep = ',')
sql_insert = f'''INSERT INTO `{TABLE_CUSTOMER}`(id, name, email) 
VALUES '''

# insert 문
conn = connection.MySQLConnection(
    user     = USER,
    password = PASSWORD,
    host     = HOST,
    database = DATABASE
    )
cur = conn.cursor()



for (id, name, email) in df_customer.values:
    # print(id, name, email)
    if int(id) == len(df_customer.values):
        sql_insert += f'''({int(id)}, '{str(name)}', '{str(email)}');'''
    else:
        sql_insert += f'''({int(id)}, '{str(name)}', '{str(email)}'), '''

cur.execute(sql_insert)
conn.commit()
conn.close()





import pandas as pd
from mysql.connector import (connection)
from important_data import *

def main():
    # ## sql 모음
    sql_0 = "DROP DATABASE `drone_project`;"
    sql_1 = "CREATE DATABASE `drone_project`;"
    sql_2 =f'''
        CREATE TABLE `{TABLE_CUSTOMER}` (
        `id` INT(11) UNSIGNED NOT NULL,
        `name` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
        `email` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_general_ci')
        COLLATE='utf8mb4_general_ci'
        ENGINE=InnoDB;
        '''
    sql_3 =f'''
    CREATE TABLE `{TABLE_WEBCAM}` (
        `id` INT(10) UNSIGNED NOT NULL,
        `label` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
        `num` INT(10) UNSIGNED ZEROFILL NOT NULL,
        `threshold` FLOAT UNSIGNED NOT NULL,
        `time` DATETIME NOT NULL,
        `latitude` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
        `longitude` VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
        `send_email` TINYINT(3) UNSIGNED ZEROFILL NOT NULL)
    COLLATE='utf8mb4_general_ci'
    ENGINE=InnoDB;
    '''

    # 기본 setting
    conn = connection.MySQLConnection(
        user     = USER,
        password = PASSWORD,
        host     = HOST,
    )
    cur = conn.cursor()

    # 0. Databse 삭제 (있으면 삭제)
    try:
        cur.execute(sql_0)   
    except Exception as e:
        print(e)

    # 1. Database 생성
    cur.execute(sql_1)   
    conn.close()

    # 2. Table 생성
    conn = connection.MySQLConnection(
        user     = USER,
        password = PASSWORD,
        host     = HOST,
        database = DATABASE
    )
    cur = conn.cursor()
    cur.execute(sql_2)
    cur.execute(sql_3)
    conn.close()

if __name__ == '__main__':
    main()
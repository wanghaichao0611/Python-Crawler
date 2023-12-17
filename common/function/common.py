import time
import pymysql
import os
import shutil
import pymysql
import common.constant.globals as constant
from conf.settings import DATABASES

seq = 0
last_timestamp = -1


def til_next_millis(last_timestamp):
    timestamp = int(time.time() * 1000)
    while timestamp <= last_timestamp:
        timestamp = int(time.time() * 1000)
    return timestamp


# Snowflake id
def gen_uuid():
    global seq
    global last_timestamp
    timestamp = int(time.time() * 1000)
    if last_timestamp > timestamp:
        raise ValueError("Clock moved backwards. Refusing to generate id")
    if last_timestamp == timestamp:
        seq = (seq + 1) & 0xFFF  # 4095
        if seq == 0:
            timestamp = til_next_millis(last_timestamp)
    else:
        seq = 0
    last_timestamp = timestamp
    timestamp -= 1546300800000

    return (timestamp << 22) | (0 << 12) | seq


# def mysql connection
def get_mysql_connect():
    mysql = DATABASES.get('mysql')
    conn = pymysql.connect(host=mysql.get('host'), port=mysql.get('port'),
                           user=mysql.get('user'), password=mysql.get('password'),
                           database=mysql.get('database'), charset=mysql.get('charset'))
    return conn


# clear files
def clear_files(folder_path):
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
        print(f"success: {folder_path}")
    except Exception as e:
        print(f"{folder_path} error：{str(e)}")


# clear folders
def remove_dir(dir_path):
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
        print("Directory removed successfully")
    else:
        print("Invalid directory path")


# load css
def getStyleCss():
    with open('../../conf/style.css', 'r') as f:
        return f.read()


# truncate and inset into mysql papers
def truncate_and_insert_info_mysql(data_list):
    conn = get_mysql_connect()
    cursor = conn.cursor()
    sql_list = []
    for data in data_list:
        sql_list.append(
            (data.id, data.title, data.content, data.star, data.paper_url, data.pdf_url, data.github_url, data.date,
             data.create_time))
    try:
        cursor.execute(constant.TRUNCATE_PAPERS_WINT_CODE_SQL)
        cursor.executemany(constant.BATCH_INSET_PAPERS_WINT_CODE_SQL, sql_list)
        conn.commit()
    except pymysql.MySQLError as err:
        conn.rollback()
        print(type(err), err)
    finally:
        cursor.close()
        conn.close()

__author__ = 'alex'

import sqlite3, file_manager, config

conn = sqlite3.connect(config.database_location, check_same_thread=False)
c = conn.cursor()

def get_all():
    c.execute("SELECT * FROM db_file")
    files = []
    for query_result in c.fetchall():
        file = file_manager.File(query_result[2], query_result[1], query_result[3], query_result[4])
        files.append(file)
    return files

def get_file(guid):
    c.execute("SELECT * FROM db_file WHERE file_name=?", (guid,))
    query_result = c.fetchone()
    return file_manager.File(query_result[2], query_result[1], query_result[3], query_result[4])

def get_oldest():
    c.execute("SELECT * FROM db_file ORDER BY unix_time_created LIMIT 1")
    query_result = c.fetchone()
    return file_manager.File(query_result[2], query_result[1], query_result[3], query_result[4])

def add_file(file):
    c.execute("INSERT INTO db_file (file_name, display_name, file_size, unix_time_created) VALUES (?,?,?,?)",
              (file.file_name, file.display_name, file.file_size, file.timestamp))
    conn.commit()

def delete_row(file_name):
    c.execute("DELETE FROM db_file WHERE file_name=?", (file_name,))
    conn.commit()
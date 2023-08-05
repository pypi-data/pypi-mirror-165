This package using MySQLdb interface to connect to database.
This module will give convenience to fetch data as list (fetch_dbdata_list) and export it to text file (write_dbdata_file), or do all in 1 go using fetch_dbdata_file.

CONTENTS:
1st Module - mydb.py

def fetch_dbdata_file(sql, db_credential, output_filename, mode="w", delimiter="\t") # all in one
def fetch_dbdata_list(sql, db_credential, header=True)
def write_dbdata_file(data_as_list, output_filename, mode="w", header_as_list=[], delimiter="\t")
def write_list_file(list_data, output_filename, mode="w")

2st Module - mydbconn.py

def set_logger(log_name)
class Connect_DB: MySQLdb connection with additional feature to create log file

import MySQLdb
import os


def fetch_dbdata_list(sql, db_credential, header=True):
    """ Fetch data from database from the given sql and db_credential

    parameters:
    sql (str): mysql query
    db_credential (dict): database credential
    ie. 
    db_credential = {  #
        "user": "admin",
        "password": "password",
        "host": "127.0.0.1",
        "db": "mydb",
    }
    header (bool) with default as True

    returns list of data tuples then you can export the data to files using export_data_file
    i.e.:   return_data = export_db_list(sql, header=True)
            write_dbdata_file(return_data, output_filename, mode="w", header_as_list=[], delimiter="\t")
    """
    try:
        header_list = []
        data_list = []  # list of list
        conn = MySQLdb.connect(**db_credential)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        record_set = cursor.fetchall()
        count = 0
        for record in record_set:
            count += 1
            if (header and count == 1):
                header_list.append(record.keys())
            data_list.append(record.values())
        return header_list + data_list  # combined header w/ data
    finally:
        conn.close()


# direct output to file (one solution)
def fetch_dbdata_file(sql, db_credential, output_filename, mode="w", delimiter="\t"):
    """ Fetch data from database from the given sql and db_credential and save it as file

    parameters:
    sql (str): mysql query
    db_credential (dict): database credential
    ie. 
    db_credential = {  #
        "user": "admin",
        "password": "password",
        "host": "127.0.0.1",
        "db": "mydb",
    }
    output_filename (str): output file name, ie. output.txt 
    mode(str): file stream mode with default = "w"
    delimiter (str): default as tab delimiter

    returns dbdata as text file
    """
    try:
        conn = MySQLdb.connect(**db_credential)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        record_set = cursor.fetchall()
        count = 0
        ori_umask = os.umask(0)
        with open(output_filename, mode, os.O_RDWR | os.O_CREAT) as fw:
            for record in record_set:
                count += 1
                if (count == 1):
                    fw.write(delimiter.join(str(item)
                                            for item in record.keys())+'\n')
                fw.write(delimiter.join(str(item)
                         for item in record.values())+'\n')
    finally:
        os.umask(ori_umask)
        conn.close()

import logging
import MySQLdb


def set_logger(log_name):
    """ setting up logger for recording database execution with format %(asctime)s: %(levelname)s: %(message)s
    parameters:
    log_name (str): logger file name ie. logfile.log

    returns: logging.Logger object
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    file_handler = logging.FileHandler(log_name)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


class Connect_DB:
    """ Blueprint to create MySQLdb connection object with logger. 
    the benefit of using this class that it will create a log file for each execution.

    parameters:
    my_logger (logging.Logger) with default = None
    """

    def __init__(self, db_credential: dict, my_logger: logging.Logger = None):
        self.logger = my_logger
        self.conn = None
        self.cursor = None
        self.credential = db_credential
        self.__connect(db_credential)

    def __connect(self, db_credential: dict):  # private
        self.conn = MySQLdb.connect(**db_credential)
        self.conn.ssl_mode = "DISABLED"
        self.conn.ping(True)

        self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.conn.autocommit(True)
        if self.logger:
            self.logger.info(
                f"Connection to {db_credential['database']} has been created.")

    def execute(self, sql: str, data=None):
        if self.logger:
            text = f"{sql} {data}" if data else f"{sql}"
            self.logger.info(text)
        return self.cursor.execute(sql, data)

    def fetchall(self, sql: str, data=None):
        self.execute(sql, data)
        return self.cursor.fetchall()

    def fetchone(self, sql: str, data=None):
        self.execute(sql, data)
        return self.cursor.fetchone()

    def update(self, sql: str, data=None):
        rows_count = self.execute(sql, data)
        self.conn.commit()
        if self.logger:
            self.logger.info(f"Updated {rows_count} rows.")
        return rows_count

    def insert(self, sql: str, data=None):
        self.execute(sql, data)
        last_row_id = self.cursor.lastrowid
        self.conn.commit()
        if self.logger:
            self.logger.info(f"Insert id = {last_row_id}")
        return last_row_id

    def close(self):
        if self.conn.open:
            self.conn.close()
            self.conn = None
        if self.logger:
            self.logger.info(
                f"Close connection to {self.credential['database']}.")

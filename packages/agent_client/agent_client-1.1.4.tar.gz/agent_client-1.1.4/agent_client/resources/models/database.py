# coding=utf-8
# pylint: disable=broad-except, import-error
import os
import yaml
from datetime import datetime, timezone, timedelta
import threading
import pymysql as mysql


class SqlConnection(object):

    def __init__(self, db_name="production_test"):
        self.host = None
        self.port = None
        self.user = None
        self.passwd = None
        self.db_name = db_name
        self.get_data_base_config()
        self.conn = mysql.connect(host=self.host, port=self.port, user=self.user,
                                  passwd=self.passwd, db=self.db_name, charset="utf8")
        self.cursor = self.conn.cursor()

    def get_data_base_config(self):
        config_file = os.path.join(os.path.dirname(__file__), "../..", "configuration", "database.yaml")
        with open(config_file, encoding='utf-8') as f:
            db_config = yaml.safe_load(f)
            self.host = db_config["mysql"]["host"]
            self.port = db_config["mysql"]["port"]
            self.user = db_config["mysql"]["user"]
            self.passwd = db_config["mysql"]["passwd"]

    def reconnect(self):
        self.conn = mysql.connect(host=self.host, port=self.port, user=self.user,
                                  passwd=self.passwd, db=self.db_name, charset="utf8")
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def ping(self):
        return self.conn.ping()

    def get_datetime(self):
        tz = timezone(timedelta(hours=+8))
        current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return current_time

    def insert_to_table(self, table, **kwargs):
        col_str, value_str = self._covert_dict_2_insert_string(**kwargs)
        insert_command = "INSERT INTO `{}` ({}) VALUES({})".format(table, col_str, value_str)
        self.cursor.execute(insert_command)
        self.conn.commit()

    @staticmethod
    def _covert_dict_2_insert_string(**kwargs):
        col_str = ""
        value_str = ""
        for key, value in kwargs.items():
            col_str = "`{}`".format(key) if col_str == "" else "{},`{}`".format(col_str, key)
            value_str = "'{}'".format(value) if value_str == "" else "{},'{}'".format(value_str, value)
        return col_str, value_str

    @staticmethod
    def _covert_dict_2_update_string(**kwargs):
        update_str = ""
        for key, value in kwargs.items():
            temp_str = "{}='{}'".format(key, value)
            update_str = "{},{}".format(update_str, temp_str) if update_str != "" else temp_str
        return update_str

    def insert_test_result(self, **kwargs):
        self.insert_to_table("test_results", **kwargs)

    def exist_key(self, test_key):
        sql_command = "SELECT test_key from test_results WHERE test_key='{}'".format(test_key)
        self.cursor.execute(sql_command)
        result = self.cursor.fetchone()
        return result

    def update_test_states(self, test_key, **kwargs):
        str_date = ""
        for key, value in kwargs.items():
            temp_str = "{}='{}'".format(key, value)
            str_date = temp_str if str_date == "" else "{},{}".format(str_date, temp_str)
            if key == "result":
                if value == 3:
                    temp_str = "{}='{}'".format("start_time", self.get_datetime())
                    str_date = "{},{}".format(str_date, temp_str)
                elif value in [0, 1]:
                    temp_str = "{}='{}'".format("end_time", self.get_datetime())
                    str_date = "{},{}".format(str_date, temp_str)
        update_command = "UPDATE test_results SET {} where test_key='{}'".format(str_date, test_key)
        self.cursor.execute(update_command)
        self.conn.commit()

    def update_test_to_abnormal_end(self, ip_addr):
        update_command = "UPDATE test_results SET result='15' where ip='{}' AND (result='3' OR result='2')".format(ip_addr)
        self.cursor.execute(update_command)
        self.conn.commit()

    def create_table(self, table_name, col_attrs):
        str_col = None
        for item in list(col_attrs):
            if str_col is None:
                str_col = "`{}` {}".format(item["name"], item["type"])
            else:
                str_col = "{}, `{}` {}".format(str_col, item["name"], item["type"])
        command = "CREATE TABLE `{}` ({})".format(table_name, str_col)
        self.cursor.execute(command)
        self.conn.commit()

    def get_last_index(self, table_name='tests'):
        command = "select `index` from {} ORDER by `index` desc".format(table_name)
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        index = result[0] if result else 0
        return index

    def is_exist_table(self, table):
        sql_command = "select * from information_schema.TABLES  where TABLE_NAME='{}';".format(table)
        self.cursor.execute(sql_command)
        gets = self.cursor.fetchone()
        result = True if gets else False
        return result

    def execute_sql_command(self, command):
        results = list()
        try:
            self.conn.ping()
            self.cursor.execute(command)
            results = self.cursor.fetchall()
        except BaseException as message:
            print(message)
        return results



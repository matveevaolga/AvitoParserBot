from config import db_config
import pymysql


class Bd:
    def __init__(self):
        self.connect = None

    def open_connect(self):
        try:
            self.connect = pymysql.connect(
                host=db_config["host"],
                user=db_config["user"],
                password=db_config["password"],
                database=db_config["db_name"],
            )

        except Exception as ex:
            print(ex)

    def close_connect(self):
        try:
            self.connect.close()
        except Exception as ex:
            print(ex)

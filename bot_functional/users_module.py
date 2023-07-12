from bot_functional.config import db_config
import pymysql


class Users:
    def __init__(self):
        self.connect = None
        self.open_connect()

    def open_connect(self):
        # установление соединения с бд с помощью данных из db_config
        try:
            self.connect = pymysql.connect(
                host=db_config["host"],
                user=db_config["user"],
                password=db_config["password"],
                database=db_config["db_name"],
                autocommit=True
            )

        except Exception as ex:
            print(ex)

    def close_connect(self):
        try:
            self.connect.close()
        except Exception as ex:
            print(ex)

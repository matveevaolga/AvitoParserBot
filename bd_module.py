import asyncio

from config import db_config
import aiomysql, asyncio


class Bd:
    def __init__(self):
        self.connect = None
        self.loop = None

    async def open_connect(self):
        # установление соединения с бд с помощью данных из db_config
        try:
            self.loop = asyncio.get_event_loop()
            self.connect = await aiomysql.connect(
                host=db_config["host"],
                user=db_config["user"],
                password=db_config["password"],
                db=db_config["db_name"],
                loop=self.loop,
                autocommit=True
            )

        except Exception as ex:
            print(ex, "open")

    def close_connect(self):
        try:
            self.connect.close()
        except Exception as ex:
            print(ex, "close")

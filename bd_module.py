import asyncio

from config import db_config
import aiomysql, asyncio


class Bd:
    def __init__(self):
        self.pool = None
        self.loop = None

    async def open_connect(self):
        # установление соединения с бд с помощью данных из db_config
        try:
            self.loop = asyncio.get_event_loop()
            self.pool = await aiomysql.create_pool(
                host=db_config["host"],
                user=db_config["user"],
                password=db_config["password"],
                db=db_config["db_name"],
                loop=self.loop,
                autocommit=True,
                minsize=0,
                maxsize=10,
            )

        except Exception as ex:
            print(ex, "open")

    def close_connect(self):
        try:
            self.pool.close()
        except Exception as ex:
            print(ex, "close")

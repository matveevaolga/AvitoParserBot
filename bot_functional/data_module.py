from db_functional.db_functions import Functions
from aiogram.methods.send_photo import SendPhoto
from aiogram.types import BufferedInputFile

bd_functions: Functions = Functions()


async def send_data(chat_id, cursor):
    try:
        # получение информации, запрошенной в чате с id chat_id, с помощью функции get_data
        cursor.execute(f"select current_category from users where user_id='{chat_id}';")
        category = cursor.fetchone()[0]
        # с этого номера начнется получение объявлений из бд
        cursor.execute(f"select {category} from users where user_id='{chat_id}';")
        bd_functions.start_getting_data = cursor.fetchone()[0]
        cursor.execute(f"select current_amount from users where user_id='{chat_id}';")
        need_to_get = cursor.fetchone()[0]
        # при следующем обращение к данной категории получение объявлений из базы данных начнется со сдвигом с предыдущего
        # номера на need_to_get
        cursor.execute(f"update users set {category}={bd_functions.start_getting_data+need_to_get} where user_id='{chat_id}';")
        adds = bd_functions.get_data(category, need_to_get)
        # составление сообщений из полученных данных и их отправка в чат
        for add in adds.values():
            photo: BufferedInputFile = BufferedInputFile(file=add["photo"], filename=f"{add[f'{category}_id']}")
            caption: str = f"{add['title']}\nЦена: {add['price']}\n{add['location']}\n{add['link']}"
            await SendPhoto(chat_id=chat_id, photo=photo, caption=caption)
    except Exception as ex:
        print(ex, "send_data")

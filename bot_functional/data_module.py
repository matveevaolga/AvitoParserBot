from db_functional.db_functions import Functions
from aiogram.methods.send_photo import SendPhoto
from aiogram.types import BufferedInputFile

bd_functions: Functions = Functions()


async def send_data(user_id, category, need_to_get, start_getting_data):
    try:
        # с этого номера начнется получение объявлений из бд
        bd_functions.start_getting_data = start_getting_data - need_to_get + 1
        adds = await bd_functions.get_data(category, need_to_get, user_id)
        # составление сообщений из полученных данных и их отправка в чат
        for add in adds.values():
            photo: BufferedInputFile = BufferedInputFile(file=add["photo"], filename=f"{add[f'{category}_id']}")
            caption: str = f"{add['title']}\nЦена: {add['price']}\n{add['location']}\n{add['link']}"
            await SendPhoto(chat_id=user_id, photo=photo, caption=caption)
    except Exception as ex:
        print(ex, "send_data")

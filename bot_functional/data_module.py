from db_functional.db_functions import Functions
from bot_functional.users_module import users
from aiogram.methods.send_photo import SendPhoto
from aiogram.types import BufferedInputFile

bd_functions: Functions = Functions()


async def send_data(chat_id):
    # получение информации, запрошенной в чате с id chat_id, с помощью функции get_data
    current_user = users[chat_id]
    category = current_user["current_category"]
    # с этого номера начнется получение объявлений из бд
    bd_functions.start_getting_data = current_user["start_from"][category]
    need_to_get = current_user["current_amount"]
    adds = bd_functions.get_data(category, need_to_get)
    # при следующем обращение к данной категории получение объявлений из базы данных начнется со сдвигом с предыдущего
    # номера на need_to_get
    current_user["start_from"][category] += need_to_get
    # составление сообщений из полученных данных и их отправка в чат
    for add in adds.values():
        photo: BufferedInputFile = BufferedInputFile(file=add["photo"], filename=f"{add[f'{category}_id']}")
        caption: str = f"{add['title']}\nЦена: {add['price']}\n{add['location']}\n{add['link']}"
        await SendPhoto(chat_id=chat_id, photo=photo, caption=caption)

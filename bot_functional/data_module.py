from db_functional.db_functions import Functions
from bot_functional.users_module import users
from aiogram.methods.send_photo import SendPhoto
from aiogram.types import BufferedInputFile

bd_functions: Functions = Functions()


async def send_data(user_id):
    current_user = users[user_id]
    category = current_user["current_category"]
    bd_functions.start_getting_data = current_user["start_from"][category]
    need_to_get = current_user["current_amount"]
    adds = bd_functions.get_data(category, need_to_get)
    current_user["start_from"][category] += need_to_get
    for add in adds.values():
        photo: BufferedInputFile = BufferedInputFile(file=add["photo"], filename=f"{add[f'{category}_id']}")
        caption: str = f"{add['title']}\nЦена: {add['price']}\n{add['location']}\n{add['link']}"
        await SendPhoto(chat_id=user_id, photo=photo, caption=caption)

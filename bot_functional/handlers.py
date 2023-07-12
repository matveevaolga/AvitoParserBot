from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot_functional.bot_lexicon import lexicon
from aiogram import Router
from bot_functional.keyboards import categories_keyboard, number_keyboard
from bot_functional.users_module import users, user_form
from bot_functional.data_module import send_data
from transliterate import translit


router: Router = Router()


# обработка команды /start
@router.message(Command(commands="start"))
async def process_start_command(message: Message):
    # если пользователя еще нет в users, он туда добавляется
    if message.from_user.id not in users:
        users[message.from_user.id] = user_form
    # отправка клавиатуры для выбора категории объявлений
    await message.answer(text=lexicon["/start"], reply_markup=categories_keyboard)


# обработка выбора количества объявлений
@router.callback_query(lambda callback: callback.data.isdigit())
async def number_choice(callback: CallbackQuery):
    # изменение для текущего пользователя количества запрашиваемых сообщений
    users[callback.message.chat.id]["current_amount"] = int(callback.data)
    await callback.message.answer(text=callback.data)
    chat_id = callback.message.chat.id
    # удаление отправленной ранее клавиатуры с выбором кол-ва объявлений
    await callback.message.delete()
    await callback.answer()
    # вызов функции send_data из data_module для отправки необходимого кол-ва объявлений из выбранной категории
    await send_data(chat_id)


# обработка выбора пользователем категории
@router.callback_query()
async def category_choice(callback: CallbackQuery):
    await callback.message.answer(text=f"Выбраны {callback.data}.")
    # изменение для пользователя "активной" категории (категория транслируется для получения данных из бд)
    users[callback.message.chat.id]["current_category"] = translit(callback.data, reversed=True)
    # отправка клавиатуры для выбора количества объявлений
    await callback.message.answer(text=lexicon["amount"], reply_markup=number_keyboard)
    # удаление отправленной ранее клавиатуры с категориями
    await callback.message.delete()
    await callback.answer()


# удаление ненужных отправленных в чат сообщений
@router.message()
async def other_messages(message: Message):
    await message.delete()

from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot_functional.bot_lexicon import lexicon
from aiogram import Router
from bot_functional.keyboards import categories_keyboard, number_keyboard
from bot_functional.users_module import users, user_form
from bot_functional.data_module import send_data
from transliterate import translit


router: Router = Router()


@router.message(Command(commands="start"))
async def process_start_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = user_form
    await message.answer(text=lexicon["/start"], reply_markup=categories_keyboard)


@router.callback_query(lambda callback: callback.data.isdigit())
async def number_choice(callback: CallbackQuery):
    users[callback.message.chat.id]["current_amount"] = int(callback.data)
    await callback.message.answer(text=callback.data)
    chat_id = callback.message.chat.id
    await callback.message.delete()
    await callback.answer()
    await send_data(chat_id)


@router.callback_query()
async def category_choice(callback: CallbackQuery):
    await callback.message.answer(text=f"Выбраны {callback.data}.")
    users[callback.message.chat.id]["current_category"] = translit(callback.data, reversed=True)
    await callback.message.answer(text=lexicon["amount"], reply_markup=number_keyboard)
    await callback.message.delete()
    await callback.answer()


@router.message()
async def other_messages(message: Message):
    await message.delete()

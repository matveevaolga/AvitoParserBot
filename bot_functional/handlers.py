from aiogram.types import Message
from aiogram.filters import Command
from bot_functional.bot_lexicon import lexicon
from aiogram import Router
from bot_functional.keyboards import categories_keyboard

router: Router = Router()


@router.message(Command(commands="start"))
async def process_start_command(message: Message):
    await message.answer(text=lexicon["/start"], reply_markup=categories_keyboard)


@router.message()
async def send_echo(message: Message):
    await message.answer(text=lexicon["other"], reply_markup=categories_keyboard)
    await message.delete()

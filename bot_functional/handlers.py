from aiogram.types import Message
from aiogram.filters import Command
from bot_functional.bot_lexicon import lexicon
from aiogram import Router

router: Router = Router()


@router.message(Command(commands="start"))
async def process_start_command(message: Message):
    await message.answer(text=lexicon["/start"])


@router.message()
async def send_echo(message: Message):
    await message.answer(text=lexicon["other"])
    await message.delete()

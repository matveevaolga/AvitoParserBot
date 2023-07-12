from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot_functional.bot_lexicon import lexicon
from aiogram import Router
from bot_functional.keyboards import categories_keyboard, number_keyboard

router: Router = Router()


@router.message(Command(commands="start"))
async def process_start_command(message: Message):
    await message.answer(text=lexicon["/start"], reply_markup=categories_keyboard)


@router.callback_query(lambda callback: callback.data.isdigit())
async def category_choice(callback: CallbackQuery):
    await callback.message.answer(text=callback.data)
    await callback.message.delete()
    await callback.answer()


@router.callback_query()
async def category_choice(callback: CallbackQuery):
    await callback.message.answer(text=callback.data)
    await callback.message.answer(text=lexicon["amount"], reply_markup=number_keyboard)
    await callback.message.delete()
    await callback.answer()


@router.message()
async def other_messages(message: Message):
    await message.answer(text=lexicon["other"], reply_markup=categories_keyboard)
    await message.delete()

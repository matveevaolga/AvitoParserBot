from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_categories_kb() -> InlineKeyboardMarkup:
    keyboard: list[InlineKeyboardButton] = []
    categories: list = ["Собаки 🐶", "Кошки 🐱", "Грызуны 🐹", "Кролики 🐰", "Птицы 🦜"]
    for category in categories:
        new_button: InlineKeyboardButton = InlineKeyboardButton(
            text=category,
            callback_data=f"button {category.split()[0].lower()} pressed"
        )
        keyboard.append(new_button)
    keyboard_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard_builder.row(*keyboard, width=3)
    return keyboard_builder.as_markup(resize_keyboard=True)


categories_keyboard: InlineKeyboardMarkup = create_categories_kb()

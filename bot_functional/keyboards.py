from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# клавиатура для выбора категории
def create_categories_kb() -> InlineKeyboardMarkup:
    # создание массива
    keyboard: list[InlineKeyboardButton] = []
    categories: list = ["Собаки 🐶", "Кошки 🐱", "Грызуны 🐹", "Кролики 🐰", "Птицы 🦜"]
    # наполнение массива кнопками
    for category in categories:
        new_button: InlineKeyboardButton = InlineKeyboardButton(
            text=category,
            callback_data=f"{category.split()[0].lower()}"
        )
        keyboard.append(new_button)
    # формирование клавиатуры
    keyboard_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard_builder.row(*keyboard, width=3)
    return keyboard_builder.as_markup(resize_keyboard=True)


# клавиатура для выбора количества отправляемых объявлений
def create_number_kb() -> InlineKeyboardMarkup:
    # создание массива
    keyboard: list[InlineKeyboardButton] = []
    numbers: list = [1, 5, 10]
    # наполнение массива кнопками
    for number in numbers:
        new_button: InlineKeyboardButton = InlineKeyboardButton(
            text=number,
            callback_data=f"{number}"
        )
        keyboard.append(new_button)
    # формирование клавиатуры
    keyboard_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard_builder.row(*keyboard, width=3)
    return keyboard_builder.as_markup(resize_keyboard=True)


categories_keyboard: InlineKeyboardMarkup = create_categories_kb()
number_keyboard: InlineKeyboardMarkup = create_number_kb()

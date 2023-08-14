from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from bot_functional.bot_lexicon import lexicon
from aiogram import Router
from bot_functional.keyboards import categories_keyboard, number_keyboard
from bot_functional.users_module import Users
from bot_functional.data_module import send_data
from transliterate import translit
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

router: Router = Router()

users: Users = Users()
users.open_connect()
cursor: users.connect.cursor = users.connect.cursor()


# отправка статискики по запросом пользователя
@router.message(Command(commands="statistics"))
async def send_statistics(message: Message):
    try:
        # собираем в список имена всех столбцов в таблице выбранной категории
        cursor.execute(f"show columns from users")
        columns = [info[0] for info in cursor.fetchall()]
        # данные текущего пользователя
        cursor.execute(f"select * from users where user_id='{message.chat.id}';")
        info = cursor.fetchall()[0]
        by_date = info[8:]
        by_category = info[3:8]
        # создание таблиц
        by_date = {'Date': columns[8:], 'Amount': by_date}
        by_category = {'Category': [translit(x, 'ru') for x in columns[3:8]], 'Amount': by_category}
        # # define plotting region (1 row, 2 columns)
        f, axes = plt.subplots(1, 2, figsize=(20, 5))
        f.suptitle(f'Статистика запросов пользователя {message.from_user.full_name}')
        sns.lineplot(data=by_date, x='Date', y='Amount', ax=axes[0])
        sns.lineplot(data=by_category, x='Category', y='Amount', ax=axes[1])
        # сохранение и отправка графика
        plt.savefig(fname=f'C:/AvitoParserBot/graphics/figure{message.chat.id}.png')
        photo = FSInputFile(f'C:/AvitoParserBot/graphics/figure{message.chat.id}.png')
        await message.answer_photo(photo)
    except Exception as ex:
        print(ex, "send_statistics")


# обработка команды /start
@router.message(Command(commands="start"))
async def process_start_command(message: Message):
    try:
        # если пользователя еще нет в users, он туда добавляется
        form = f"select koshki from users where user_id = '{message.chat.id}';"
        if not cursor.execute(form):
            cursor.execute(f"""insert into users (user_id, current_category, current_amount, gryzuny, koshki, kroliki, """
                           f"""ptitsy, sobaki) values ('{message.chat.id}', 'koshki', 0, 1, 1, 1, 1, 1);""")
        # отправка клавиатуры для выбора категории объявлений
        await message.answer(text=lexicon["/start"], reply_markup=categories_keyboard)
    except Exception as ex:
        print(ex, "process_start_command")


# обработка выбора количества объявлений
@router.callback_query(lambda callback: callback.data.isdigit())
async def number_choice(callback: CallbackQuery):
    try:
        chat_id = callback.message.chat.id
        # изменение для текущего пользователя количества запрашиваемых сообщений
        cursor.execute(f"update users set current_amount={int(callback.data)} where user_id='{chat_id}';")

        # собираем в список имена всех столбцов в таблице выбранной категории
        cursor.execute(f"show columns from users")
        columns = [info[0] for info in cursor.fetchall()]
        # проверка на наличие в таблице текущей даты и обновление кол-ва объявлений в этот день
        today = str(datetime.date.today())
        today = today.replace('-', '_')
        today = '2023_08_17'
        print(columns)
        if today not in columns:
            cursor.execute(f"alter table users add column {today} int default 0;")
        cursor.execute(f"select {today} from users where user_id='{chat_id}';")
        curr = cursor.fetchone()[0]
        cursor.execute(f"update users set {today}={curr + int(callback.data)} where user_id = '{chat_id}';")

        await callback.message.answer(text=callback.data)
        # удаление отправленной ранее клавиатуры с выбором кол-ва объявлений
        await callback.message.delete()
        await callback.answer()
        # вызов функции send_data из data_module для отправки необходимого кол-ва объявлений из выбранной категории
        await send_data(chat_id, cursor)
    except Exception as ex:
        print(ex, "number_choice")


# обработка выбора пользователем категории
@router.callback_query()
async def category_choice(callback: CallbackQuery):
    try:
        await callback.message.answer(text=f"Выбраны {callback.data}.")
        # изменение для пользователя "активной" категории (категория транслируется для получения данных из бд)
        cursor.execute(f"update users set current_category='{translit(callback.data, reversed=True)}'"
                       f" where user_id='{callback.message.chat.id}';")
        # отправка клавиатуры для выбора количества объявлений
        await callback.message.answer(text=lexicon["amount"], reply_markup=number_keyboard)
        # удаление отправленной ранее клавиатуры с категориями
        await callback.message.delete()
        await callback.answer()
    except Exception as ex:
        print(ex, "category_choice")


# удаление ненужных отправленных в чат сообщений
@router.message()
async def other_messages(message: Message):
    try:
        await message.delete()
    except Exception as ex:
        print(ex, "other_messages")

import matplotlib.dates
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
        user_id = message.chat.id
        cursor.execute(f"SELECT date, amount FROM queries where user_id = {user_id};")
        amount_by_date = {}
        for date, amount in cursor.fetchall():
            amount_by_date[date] = amount_by_date.get(date, 0) + amount
        # создание таблицы
        dates = list(amount_by_date.keys())
        amounts = list(amount_by_date.values())
        print(dates)
        step = 5
        date_format = '%Y-%m-%d'
        start_date = datetime.datetime.strptime(dates[0], date_format)
        end_date = datetime.datetime.strptime(dates[-1], date_format) + datetime.timedelta(days=step)
        dates = [datetime.datetime.strptime(d, date_format) for d in dates]
        print(type(dates[0]))
        dates_list = []
        # добавление в список диапазона дат
        while start_date <= end_date:
            dates_list.append(start_date)
            start_date += datetime.timedelta(days=step)
        print(dates_list)
        dx = matplotlib.dates.date2num(dates_list)
        by_date = {'Дата': dx, 'Количество запросов': amounts}
        plt.figure(figsize=(10, 10))
        plt.yticks([x for x in range(min(amounts), max(amounts) + step + 1, step)])
        plt.xticks(dates)
        plt.ylabel('Количество запросов')
        plt.xlabel('Дата')
        plt.suptitle(f'Статистика запросов пользователя {message.from_user.full_name}')
        sns.pointplot(data=by_date, y='Количество запросов', x='Дата')
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
        form = f"SELECT user_id FROM users WHERE user_id = {message.chat.id};"
        cursor.execute(form)
        if not cursor.fetchone():
            cursor.execute(f"INSERT users (user_id, fav_category, all_count, fav_category_count) VALUES ({message.chat.id}, 'koshki', DEFAULT, DEFAULT);")
        # отправка клавиатуры для выбора категории объявлений
        await message.answer(text=lexicon["/start"], reply_markup=categories_keyboard)
    except Exception as ex:
        print(ex, "process_start_command")


# обработка выбора количества объявлений
@router.callback_query(lambda callback: callback.data.isdigit())
async def number_choice(callback: CallbackQuery):
    try:
        user_id = callback.message.chat.id
        amount = int(callback.data)
        # получение id последнего запроса
        cursor.execute(f"select max(query_id) from queries where user_id = {user_id};")
        last_query = cursor.fetchone()[0]
        # увеличение общего кол-ва запросов текущего пользователя
        cursor.execute(f"update users set all_count=all_count+{amount} where user_id={user_id};")
        # установка кол-ва запрашиваемых объявлений для текущего запроса
        cursor.execute(f"update queries set amount={amount} where query_id={last_query};")
        # получение кол-ва объявлений из любимой категории пользователя
        cursor.execute(f"select fav_category_count from users where user_id = {user_id};")
        current_fav_count = cursor.fetchone()[0]
        # общее кол-во запросов пользователя по текущей категории
        cursor.execute(f"select category from queries where query_id = {last_query};")
        current_category = cursor.fetchone()[0]
        cursor.execute(f"select sum(amount) from queries where user_id = {user_id} and category = '{current_category}';")
        current_category_count = cursor.fetchone()[0]
        # изменение любимой категории пользователя
        if current_category_count > current_fav_count:
            cursor.execute(f"update users set fav_category = '{current_category}' where user_id = {user_id};")
            cursor.execute(f"update users set fav_category_count = {current_category_count} where user_id = {user_id};")
        await callback.message.answer(text=callback.data)
        # удаление отправленной ранее клавиатуры с выбором кол-ва объявлений
        await callback.message.delete()
        await callback.answer()
        # вызов функции send_data из data_module для отправки необходимого кол-ва объявлений из выбранной категории
        await send_data(user_id, current_category, amount, current_category_count)
    except Exception as ex:
        print(ex, "number_choice")


# обработка выбора пользователем категории
@router.callback_query()
async def category_choice(callback: CallbackQuery):
    try:
        user_id = callback.message.chat.id
        category = callback.data
        today = str(datetime.date.today())
        await callback.message.answer(text=f"Выбраны {category}.")
        # создание нового запроса в таблице queries
        cursor.execute(f"insert queries (category, date, user_id) values ('{translit(category, language_code='ru', reversed=True)}', '{today}', {user_id});")
        # получение id последнего запроса
        cursor.execute(f"select max(query_id) from queries where user_id = {user_id};")
        # изменение id последнего запроса в таблице users для текущего пользователя
        cursor.execute(f"update users set last_request_id = {cursor.fetchone()[0]};")
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

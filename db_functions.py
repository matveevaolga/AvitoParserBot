from parser_module import Parser
from bd_module import Bd
from selenium import webdriver
import base64


class Functions:
    def __init__(self):
        # с записи под этим id начинаем вытаскивать данные из таблицы в ф-ции get_data
        self.start_getting_data = 1
        # инициализация курсора и соединения с базой данных
        self.connection = Bd()
        self.cursor = None

    # создание формы для sql-запроса на добавление записи в таблицу
    @staticmethod
    def create_form(data, category):
        form = f"insert into {category} ({category}_id, title, photo, description, price, location, link) values ("
        for key in data.keys():
            form += f"'{data[key]}'"
            if key != 'link':
                form += ', '
        form += ");"
        return form

    # создание драйвера для эмуляции действий пользователя на сайте и его парсинга
    # добавление необходимых опций для обхода блокировок
    @staticmethod
    def get_driver():
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options, executable_path=r"webdriver\chromedriver.exe")
        driver.maximize_window()
        driver.implicitly_wait(20)
        return driver

    # проверка на наличие записи в таблице
    @staticmethod
    def exists(cursor, id, category):
        form = f"SELECT id FROM {category} where {category}_id = '{id}';"
        return cursor.execute(form)

    def insert_data(self, category, numb):
        self.connection.open_connect()
        self.cursor = self.connection.connect.cursor()
        try:
            driver = Functions.get_driver()
            parser = Parser(category, driver)
            # парсинг продолжается, пока в таблицу выбранной категории не добавится необходимое кол-во объявлений
            while numb != 0:
                try:
                    # переход на страницу сайта с выбранной категорией
                    driver.get(f"https://avito.ru/moskva/{category}")
                    # парсинг объявления
                    data = parser.parse_data()
                    # если объявление уже встречалось в таблице выбранной категории, переход
                    # к парсингу следующего объявления
                    if Functions.exists(self.cursor, data[f'{category}_id'], category):
                        print("Has already been added", data[f'{category}_id'])
                    # иначе добавляем элемент в таблицу
                    else:
                        form = Functions.create_form(data, category)
                        self.cursor.execute(form)
                        numb -= 1
                        print(f"Successfully inserted, {numb} left")
                except Exception as ex:
                    print("Inserting error", ex)
            self.connection.connect.commit()
            driver.close()
        except Exception as ex:
            print(ex)

    def get_data(self, category, numb):
        try:
            self.connection.open_connect()
            self.cursor = self.connection.connect.cursor()
            # собираем в список имена всех столбцов в таблице выбранной категории
            self.cursor.execute(f"show columns from {category}")
            columns = [info[0] for info in self.cursor.fetchall()]
            result = {}
            # продолжаем вытаскивать записи из таблицы, пока не наберется нужное кол-во объявлений,
            # начиная с записи под id start_getting_data (id = порядковый номер записи)
            end_getting_data = self.start_getting_data + numb
            while self.start_getting_data < end_getting_data:
                cur = {}
                # проверка на наличие записи в таблице с нужным id
                form = f"select * from {category} where id = '{self.start_getting_data}';"
                if self.cursor.execute(form):
                    # запись есть => получение данных из нее в row
                    row = list(self.cursor.fetchone())
                    # декодирование первой фотографии объявления
                    row[3] = base64.decodebytes(row[3])
                    # запись значений из row в словарь cur под соответствующими колонками
                    for value, column in zip(row, columns):
                        cur[column] = value
                    # запись cur в result под уникальным category_id (id объявления на странице выбранной категории)
                    result[cur[f'{category}_id']] = cur
                    self.start_getting_data += 1
                # если записи нет, значит в таблице больше не осталось невыбранных записей,
                # и необходимо дополнить ее, используя ф-ю insert_data
                else:
                    print(f"Need to insert {end_getting_data - self.start_getting_data} more ads")
                    self.insert_data(category, end_getting_data - self.start_getting_data)
            self.connection.close_connect()
            return result
        except Exception as ex:
            print(ex)

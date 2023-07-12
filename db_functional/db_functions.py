from parsing.parser_module import Parser
from db_functional.bd_module import Bd
from selenium import webdriver
import base64


class Functions:
    def __init__(self):
        # с записи под этим id начинаем вытаскивать данные из таблицы в ф-ции get_data
        self.start_getting_data = 1
        # инициализация курсора и соединения с базой данных
        self.connection = Bd()
        self.cursor = self.connection.connect.cursor()
        self.driver = Functions.get_driver()

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

    def insert_data(self, category, numb):
        try:
            parser = Parser(self.driver, self.cursor)
            # парсинг объявлений
            # в data находятся numb объявлений
            data = parser.parse_data(numb, category)
            for ad in data:
                try:
                    # добавление элемента в таблицу
                    form = Functions.create_form(ad, category)
                    self.cursor.execute(form)
                    numb -= 1
                    print(f"Successfully inserted {ad[f'{category}_id']} {numb} left")
                except Exception as ex:
                    print("Inserting error", ex)
        except Exception as ex:
            print(ex, "insert_data")

    def get_data(self, category, numb):
        try:
            # собираем в список имена всех столбцов в таблице выбранной категории
            self.cursor.execute(f"show columns from {category}")
            columns = [info[0] for info in self.cursor.fetchall()]
            result = {}
            # продолжаем вытаскивать записи из таблицы, пока не наберется нужное кол-во объявлений,
            # начиная с записи под порядковым номером записи start_getting_data (столбец id)
            end_getting_data = self.start_getting_data + numb
            while self.start_getting_data < end_getting_data:
                cur = {}
                # проверка на наличие записи в таблице с нужным порядковым номером
                form = f"select * from {category} where id = '{self.start_getting_data}';"
                if self.cursor.execute(form):
                    # запись есть => получение данных из нее в row
                    row = list(self.cursor.fetchone())
                    # декодирование первой фотографии объявления
                    row[3] = base64.decodebytes(row[3])
                    # запись значений из row в словарь cur под соответствующими колонками
                    for value, column in zip(row, columns):
                        cur[column] = value
                    # запись cur в result под уникальным category_id (id
                    # объявления на странице выбранной категории авито)
                    result[cur[f'{category}_id']] = cur
                    self.start_getting_data += 1
                # если записи нет, значит в таблице больше не осталось невыбранных записей,
                # и необходимо дополнить ее, используя ф-ю insert_data
                else:
                    print(f"Need to insert {end_getting_data - self.start_getting_data} more ads")
                    self.insert_data(category, end_getting_data - self.start_getting_data)
            return result
        except Exception as ex:
            print(ex, "get_data")

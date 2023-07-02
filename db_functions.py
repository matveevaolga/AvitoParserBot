from parser_module import Parser
from bd_module import Bd
from selenium import webdriver
import base64


class Functions:
    def __init__(self):
        self.start_getting_data = 1
        self.connection = Bd()
        self.cursor = None

    @staticmethod
    def create_form(data, category):
        form = f"insert into {category} ({category}_id, title, photo, description, price, location, link) values ("
        for key in data.keys():
            form += f"'{data[key]}'"
            if key != 'link':
                form += ', '
        form += ");"
        return form

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
            while numb != 0:
                try:
                    driver.get(f"https://avito.ru/moskva/{category}")
                    data = parser.parse_data()
                    if Functions.exists(self.cursor, data[f'{category}_id'], category):
                        print("Has already been added", data[f'{category}_id'])
                    else:
                        form = Functions.create_form(data, category)
                        self.cursor.execute(form)
                        numb -= 1
                        print(f"Successfully inserted, {numb} left")
                except Exception as ex:
                    print(ex)
            self.connection.connect.commit()
            driver.close()
        except Exception as ex:
            print(ex)

    def get_data(self, category, numb):
        try:
            self.connection.open_connect()
            self.cursor = self.connection.connect.cursor()
            self.cursor.execute(f"show columns from {category}")
            columns = [info[0] for info in self.cursor.fetchall()]
            result = {}
            end_getting_data = self.start_getting_data + numb
            while self.start_getting_data < end_getting_data:
                cur = {}
                form = f"select * from {category} where id = '{self.start_getting_data}';"
                if self.cursor.execute(form):
                    row = list(self.cursor.fetchone())
                    row[3] = base64.decodebytes(row[3])
                    for value, column in zip(row, columns):
                        cur[column] = value
                    result[cur[f'{category}_id']] = cur
                    self.start_getting_data += 1
                else:
                    print(f"Need to insert {end_getting_data - self.start_getting_data} more ads")
                    self.insert_data(category, end_getting_data - self.start_getting_data)
            self.connection.close_connect()
            return result
        except Exception as ex:
            print(ex)

from parser import parse_data
from bd_module import Bd
import pymysql
from selenium import webdriver


def create_form(data):
    form = f"INSERT INTO zhivotnye (animal_id, title, photo, description, price, location, link) VALUES ("
    for key in data.keys():
        form += f"'{data[key]}'"
        if key != 'link':
            form += ', '
    form += ");"
    return form


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver


def connect_and_insert(category):
    try:
        connection = Bd()
        connection.open_connect()
        cursor = connection.connect.cursor()
        numb = int(input())
        driver = get_driver()
        for i in range(numb):
            driver.get(f"https://avito.ru/moskva/{category}")
            data = parse_data(category, driver)
            form = create_form(data)
            cursor.execute(form)
            print("Successfully inserted")
        driver.close()
        connection.connect.commit()
        connection.close_connect()
    except pymysql.err.IntegrityError:
        print("There are no more new advertisements to add.")
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    category = "zhivotnye"
    connect_and_insert(category)

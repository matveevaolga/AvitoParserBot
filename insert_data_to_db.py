from parser import parse_data
from bd_module import Bd
from selenium import webdriver


def create_form(data):
    form = f"INSERT INTO {category} (animal_id, title, photo, description, price, location, link) VALUES ("
    for key in data.keys():
        form += f"'{data[key]}'"
        if key != 'link':
            form += ', '
    form += ");"
    return form


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options, executable_path=r"webdriver\chromedriver.exe")
    driver.maximize_window()
    driver.implicitly_wait(60)
    return driver


def exists(cursor, id):
    form = f"SELECT id FROM {category} where animal_id = '{id}';"
    return cursor.execute(form)


def connect_and_insert(category, numb):
    try:
        connection = Bd()
        connection.open_connect()
        cursor = connection.connect.cursor()
        driver = get_driver()
        for i in range(numb):
            driver.get(f"https://avito.ru/moskva/{category}")
            data = parse_data(category, driver)
            if exists(cursor, data['animal_id']):
                print("Has already been added")
            else:
                form = create_form(data)
                cursor.execute(form)
                print("Successfully inserted")
        driver.close()
        connection.connect.commit()
        connection.close_connect()
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    category = "zhivotnye"
    numb = int(input())
    connect_and_insert(category, numb)

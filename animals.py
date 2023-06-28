import pymysql
from config import db_config
from parser import get_data


def create_form(title, description, price, contacts, link):
    form = f"INSERT INTO info (title, description, price, contacts, link) VALUES ('{title}', '{description}'," \
           f" '{price}', '{contacts}', '{link}')"
    return form


try:
    category = "zhivotnye"
    connection = pymysql.connect(
        host=db_config[category]["host"],
        user=db_config[category]["user"],
        password=db_config[category]["password"],
        database=db_config[category]["db_name"],
    )
    print("successfully connected...")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `info` (title varchar(32), description varchar(32),"
                   "price varchar(32), metro varchar(32), link varchar(32))")

    numb = int(input())
    for i in range(numb):
        data = get_data(category)
        form = create_form(*data)
        cursor.execute(form)
    connection.commit()
except Exception as ex:
    print("Connection refused...")
    print(ex, "--")


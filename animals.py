import pymysql
from config import db_config
from parser import get_data


def create_form(title, description, price, address, metro, link):
    form = f"INSERT INTO info (title, description, price, address, metro, link) VALUES ('{title}', '{description}'," \
           f" '{price}', '{address}', '{metro}', '{link}')"
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
    cursor.execute("CREATE TABLE IF NOT EXISTS `info`(title LONGTEXT, description LONGTEXT,"
                   " price LONGTEXT, address LONGTEXT, metro LONGTEXT, link LONGTEXT);")
    numb = int(input())
    for i in range(numb):
        data = get_data(category)
        form = create_form(*data)
        cursor.execute(form)
    connection.commit()
except Exception as ex:
    print("Connection refused...")
    print(ex, "--")


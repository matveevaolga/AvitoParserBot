from parser import parse_data
from bd_module import Bd
import pymysql


def create_form(data):
    form = f"INSERT INTO zhivotnye (animal_id, title, photo, description, price, location, link) VALUES ("
    for key in data.keys():
        form += f"'{data[key]}'"
        if key != 'link':
            form += ', '
    form += ");"
    return form


def connect_and_insert(category):
    try:
        connection = Bd()
        connection.open_connect()
        cursor = connection.connect.cursor()
        numb = int(input())
        for i in range(numb):
            data = parse_data(category)
            form = create_form(data)
            cursor.execute(form)
        connection.connect.commit()
        connection.close_connect()
        print("Successfully inserted")
    except pymysql.err.IntegrityError:
        print("There are no more new advertisements to add.")


if __name__ == "__main__":
    category = "zhivotnye"
    connect_and_insert(category)

from db_functional.db_functions import Functions
import asyncio


async def main():
    category = 'zhivotnye'
    functions = Functions()
    functions.insert_data(category, 2)
    d = functions.get_data(category, 4)
    print(d.keys())

asyncio.run(main())

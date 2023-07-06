from db_functions import Functions
import asyncio


async def main():
    category = 'zhivotnye'
    functions = Functions()
    task1 = asyncio.create_task(functions.insert_data(category, 2))
    task2 = asyncio.create_task(functions.get_data(category, 4))
    print((await task2).keys())
    await task1

asyncio.run(main())

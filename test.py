from db_functions import Functions
import asyncio

# categories = ['krasota_i_zdorove', 'dlya_biznesa', 'hobbi_i_otdyh', 'tovary_dlya_detey_i_igrushki',
#           'tovary_dlya_detey_i_igrushki', 'zhivotnye']
async def main():
    category = 'zhivotnye'
    print(f"----{category}-----")
    functions = Functions()
    await functions.connection.open_connect()
    # value = await functions.get_data(f'{category}', 4)
    # await functions.insert_data(f'{category}', 2)
    # print(value.keys())
    task3 = asyncio.create_task(functions.insert_data(f'{category}', 1))
    task2 = asyncio.create_task(functions.get_data(f'{category}', 3))
    task1 = asyncio.create_task(functions.get_data(f'{category}', 2))
    await task3
    print(dict(await task2).keys())
    print(dict(await task1).keys())
    functions.connection.close_connect()

asyncio.run(main())
# почему не работает if __name__ == __main__ ?

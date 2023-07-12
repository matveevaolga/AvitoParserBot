import asyncio
from bot_functional.config import bot_config
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from bot_functional.handlers import router


async def set_main_menu(bot: Bot):
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command="/start", description="Начать искать питомца")]
    await bot.set_my_commands(main_menu_commands)


async def main():
    try:
        bot_token = bot_config["token"]
        bot = Bot(token=bot_token)
        dispatcher = Dispatcher()
        dispatcher.include_router(router)
        dispatcher.startup.register(set_main_menu)
        await dispatcher.start_polling(bot)
    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    asyncio.run(main())

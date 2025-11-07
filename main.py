# """ Запускаемый файл """
#
# from aiogram.utils import executor
# from create_bot import dp
# from root import on_startup_func
# from handlers import admin, client
#
# admin.register_handlers_admin(dp)
# client.register_handlers_client(dp)
#
#
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True, on_startup=on_startup_func)



# main.py
""" Запуск бота """

import asyncio
from create_bot import dp, bot
from root import on_startup_func
from handlers import admin, client


async def main():
    # Подключаем роутеры
    dp.include_router(admin.router)
    dp.include_router(client.router)

    await on_startup_func("Startup event")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

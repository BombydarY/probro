from aiogram import types

from create_bot import bot
from settings import ADMINS, ID_MISTAKES
import logging


def admin_check(func):
    """проверка на наличие админов в группе"""
    async def candy_wrapper(message: types.Message):
        if message.from_user.id not in ADMINS:
            await message.answer("У вас недостаточно прав!")
            return
        else:
            await func(message)

    return candy_wrapper


def error_check(func):
    """защита от ошибок"""
    async def candy_wrapper(message: types.Message):
        try:
            await func(message)
        except Exception as err:
            print (err)
            logging.error(f"Ошибка {func.__name__}:{err}")
            await bot.send_message(ID_MISTAKES, f"!!!СРОЧНО В БОТЕ.\n\n{func.__name__}: {err}")
            

    return candy_wrapper
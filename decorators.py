from aiogram import types

from settings import ADMINS


def admin_check(func):
    async def candy_wrapper(message: types.Message):
        if message.from_user.id not in ADMINS:
            await message.answer("У вас недостаточно прав!")
            return
        else:
            await func(message)

    return candy_wrapper


def error_check(func):
    async def candy_wrapper(message: types.Message):
        try:
            await func(message)
        except Exception as err:
            await message.answer(f"бросай спасброски от смерти у вас ошибка!{err}")

    return candy_wrapper


def neur_bum(func):
    async def candy_wrapper(**kwargs):
        try:
            return await func(**kwargs)
        except Exception as err:
            print(f"Ошибка в нейронной сети: {err}")

    return candy_wrapper

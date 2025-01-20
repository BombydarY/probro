from create_bot import dp, bot
from aiogram import types, Dispatcher

from decorators import admin_check


@admin_check
async def admin_panel(message: types.Message):
    await bot.send_message(message.from_user.id, 'im working')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_panel, commands=['test'])

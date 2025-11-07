from create_bot import dp, bot
from aiogram import types, Dispatcher

from decorators import admin_check

from aiogram.filters.command import Command
from aiogram import types, Router, F

router = Router()



@router.message(Command("test"))
@admin_check
async def admin_panel(message: types.Message):
    await bot.send_message(message.from_user.id, 'im working')




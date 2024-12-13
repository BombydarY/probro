from create_bot import dp
from handlers import client, admin


async def on_startup_func(_):
    """Стартовая функция"""
    print('Bot is online ->', _)


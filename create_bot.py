# from aiogram import Bot
# from aiogram.dispatcher import Dispatcher
# from settings import TOKEN
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
#
# storage = MemoryStorage()
#
# # Создание бота и диспетчера
# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot, storage=storage)



from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from settings import TOKEN

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

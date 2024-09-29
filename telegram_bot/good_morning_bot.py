from telegram_database.db import Database
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command

from config.bot_config import BOT_CONFIG
from config.db_config import DB_CONFIG


class GoodMorningBot:
    def __init__(self):
        self.bot = Bot(token=BOT_CONFIG["TOKEN"])
        self.dp = Dispatcher()
        self.db = Database(DB_CONFIG["DB_NAME"])
        self.initialize_handlers()

    def initialize_handlers(self):
        @self.dp.message(CommandStart())
        async def handle_start(message: types.Message):
            if not self.db.user_exist(message.from_user.id):
                self.db.add_user(message.from_user.id)
            #print(f'Команда - {message.text}, от {message.from_user.first_name} {message.from_user.last_name}')
            await message.answer(text=f"Приветствую Вас, {message.from_user.first_name} {message.from_user.last_name}, Вы подписались на ежедневную утреннюю рассылку краткой информации. Чтобы отписаться, просто заблокируйте бота.")
            await message.answer(text="Рассылка происходит в 6:00 по МСК!")

        @self.dp.message(Command("help"))
        async def handle_help(message: types.Message):
            #print(f'Команда - {message.text}, от {message.from_user.first_name} {message.from_user.last_name}')
            await message.answer(text="Вызвана команда помощи")
                
        @self.dp.message()
        async def handle_message(message: types.Message):
            #print(f'Сообщение - {message.text}, от {message.from_user.first_name} {message.from_user.last_name}')
            pass

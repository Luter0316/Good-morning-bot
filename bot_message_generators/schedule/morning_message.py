import asyncio

import pytz
import schedule

from telegram_database.db import Database
from bot_message_generators.message import get_message
from telegram_bot.good_morning_bot import GoodMorningBot


async def send_morning_message():
    message_text = get_message()
    bot = GoodMorningBot().bot
    users = GoodMorningBot().db.get_users()
    for row in users:
        try:
            await bot.send_message(row[0], message_text, parse_mode="Markdown")
            if int(row[1]) != 1:
                GoodMorningBot().db.set_active(row[0], 1)
        except:
            GoodMorningBot().db.set_active(row[0], 0)

schedule.every().days.at("06:00", pytz.timezone("Europe/Moscow")).do(asyncio.run, send_morning_message())
#schedule.every(5).seconds.do(asyncio.run, send_morning_message())

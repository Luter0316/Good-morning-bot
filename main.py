import asyncio
import logging

from telegram_bot.good_morning_bot import GoodMorningBot
from bot_message_generators.schedule.run_background import run_continuously


async def main():
    logging.basicConfig(level=logging.DEBUG)
    dp = GoodMorningBot().dp
    bot = GoodMorningBot().bot
    run_continuously()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

import asyncio
from aiogram import Dispatcher
from bot.loader import bot, dp
from bot.bot import router

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

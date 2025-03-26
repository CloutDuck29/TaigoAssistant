from aiogram import Router
from bot.handlers import main_commands, order_handler

router = Router()
router.include_router(main_commands.router)
router.include_router(order_handler.router)

from aiogram import Router
from bot.handlers import main_commands, order_handler, sborka_handler  # добавьте sborka_handler

router = Router()
router.include_router(main_commands.router)
router.include_router(order_handler.router)
router.include_router(sborka_handler.router)  # подключите sborka_handler


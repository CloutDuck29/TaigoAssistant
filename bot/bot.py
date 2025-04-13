from aiogram import Router
from bot.handlers import main_commands, order_handler, sborka_handler, plugin_handler, launcher_handler, build_handler, site_handler, team_handler
from bot.forms import sborshik_handler

router = Router()
router.include_router(main_commands.router)
router.include_router(order_handler.router)
router.include_router(sborka_handler.router)
router.include_router(plugin_handler.router)
router.include_router(launcher_handler.router)
router.include_router(build_handler.router)
router.include_router(site_handler.router)
router.include_router(team_handler.router)
router.include_router(sborshik_handler.router)


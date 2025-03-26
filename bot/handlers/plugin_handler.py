# plugin_handler.py

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from bot.keyboards import minecraft_menu, yes_no_menu, main_menu
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID

router = Router()

# Обработчик для заказа плагина (аналогично сборке)
@router.message(OrderState.waiting_for_category)
async def process_plugin_category(message: types.Message, state: FSMContext):
    category = message.text
    if category == "Плагин":
        await message.answer("📋 Введите название проекта:", reply_markup=types.ReplyKeyboardRemove())
        await state.update_data(category=category)
        await state.set_state(OrderState.waiting_for_name)
    else:
        await message.answer("Пожалуйста, выберите категорию.", reply_markup=minecraft_menu)

# Дальше идет код, аналогичный обработчику для сборки и лаунчера.

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from bot.keyboards import project_type_menu, minecraft_menu, software_menu, main_menu
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID

router = Router()

@router.message(lambda message: message.text == "📝 Заказать")
async def order_button(message: types.Message, state: FSMContext):
    await message.answer("Выберите тип проекта:", reply_markup=project_type_menu)
    await state.set_state(OrderState.waiting_for_project_type)

@router.message(OrderState.waiting_for_project_type)
async def process_project_type(message: types.Message, state: FSMContext):
    if message.text == "🟢 Minecraft":
        await message.answer("Выберите категорию:", reply_markup=minecraft_menu)
        await state.update_data(project_type="Minecraft")
        await state.set_state(OrderState.waiting_for_category)
    elif message.text == "🔵 ПО":
        await message.answer("Выберите категорию:", reply_markup=software_menu)
        await state.update_data(project_type="ПО")
        await state.set_state(OrderState.waiting_for_category)
    else:
        await message.answer("Пожалуйста, выберите один из типов проекта.", reply_markup=project_type_menu)

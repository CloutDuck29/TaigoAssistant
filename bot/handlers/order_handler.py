from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
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
        await state.set_state(OrderState.waiting_for_po)
    else:
        await message.answer("Пожалуйста, выберите один из типов проекта.", reply_markup=project_type_menu)

@router.message(OrderState.waiting_for_category)
async def process_build_category(message: types.Message, state: FSMContext):
    category = message.text
    if category == "Сборка":
        await message.answer("📋 Введите название проекта", reply_markup=ReplyKeyboardRemove())
        await state.update_data(category=category)
        await state.set_state(OrderState.waiting_for_name)

    elif category == "Плагин":
        await message.answer("📋 Введите название плагина", reply_markup=ReplyKeyboardRemove())
        await state.update_data(category=category)
        await state.set_state(OrderState.waiting_for_namePlugin)

    elif category == "Лаунчер":
        await message.answer("📋 Введите название лаунчера", reply_markup=ReplyKeyboardRemove())
        await state.update_data(category=category)
        await state.set_state(OrderState.waiting_for_nameLauncher)

    elif category == "Постройка":
        await message.answer("📋 Введите требуемый тип постройки", reply_markup=ReplyKeyboardRemove())
        await state.update_data(category=category)
        await state.set_state(OrderState.waiting_for_typeBuild)

    else:
        await message.answer("Пожалуйста, выберите категорию.", reply_markup=minecraft_menu)


@router.message(OrderState.waiting_for_po)
async def process_po_category(message: types.Message, state: FSMContext):
    category = message.text
    if category == "Сайт":
        await message.answer("📋 Введите название сайта", reply_markup=ReplyKeyboardRemove())
        await state.update_data(category=category)
        await state.set_state(OrderState.waiting_for_nameSite)

    elif category == "Игра":
        await message.answer("Извините, кнопка не работает - обратитесь к @taigo_official", reply_markup=ReplyKeyboardRemove())

    elif category == "Приложение":
        await message.answer("Извините, кнопка не работает - обратитесь к @taigo_official", reply_markup=ReplyKeyboardRemove())

    else:
        await message.answer("Пожалуйста, выберите категорию.", reply_markup=software_menu)

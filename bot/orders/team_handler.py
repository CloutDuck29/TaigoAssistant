from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from bot.keyboards import project_type_menu, minecraft_menu, software_menu, main_menu, team_menu, team_minecraft_menu, team_po_menu, team_admin_menu
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID

router = Router()

@router.message(lambda message: message.text == "🖥 Вступить в команду")
async def team_button(message: types.Message, state: FSMContext):
    await message.answer("Выберите сферу:", reply_markup=team_menu)
    await state.set_state(OrderState.waiting_for_teamType)

@router.message(OrderState.waiting_for_teamType)
async def process_team_type(message: types.Message, state: FSMContext):
    if message.text == "🎮 Minecraft":
        await message.answer("Выберите должность:", reply_markup=team_minecraft_menu)
        await state.update_data(category="Minecraft")
        await state.set_state(OrderState.waiting_for_minecraftType)
    elif message.text == "🛠 Разработчики":
        await message.answer("Извините, на данный момент мы не набираем специалистов данного типа - обратитесь к @taigo_official", reply_markup=main_menu)

    elif message.text == "👩🏻‍✈️ Администрация":
        await message.answer("Извините, на данный момент мы не набираем специалистов данного типа - обратитесь к @taigo_official", reply_markup=main_menu)

    else:
        await message.answer("Пожалуйста, выберите один из типов проекта.", reply_markup=team_menu)

@router.message(OrderState.waiting_for_minecraftType)
async def process_minecraft_type(message: types.Message, state: FSMContext):
    category = message.text
    if category == "Специалист по сборкам":
        await message.answer("📋 Введите свое ФИО", reply_markup=ReplyKeyboardRemove())
        await state.update_data(category=category)
        await state.set_state(OrderState.waiting_for_fio)

    elif category == "Разработчик плагинов":
        await message.answer("📋 Введите свое ФИО", reply_markup=ReplyKeyboardRemove())
        await state.update_data(category=category)
        await state.set_state(OrderState.waiting_for_fioPlugin)  # Изменено состояние

    elif category == "Специалист по постройкам":
        await message.answer("Извините, кнопка не работает - обратитесь к @taigo_official", reply_markup=main_menu)

    elif category == "Разработчик модов":
        await message.answer("Извините, кнопка не работает - обратитесь к @taigo_official", reply_markup=main_menu)

    elif category == "Разработчик лаунчеров":
        await message.answer("Извините, кнопка не работает - обратитесь к @taigo_official", reply_markup=main_menu)

    else:
        await message.answer("Пожалуйста, выберите категорию.", reply_markup=team_minecraft_menu)

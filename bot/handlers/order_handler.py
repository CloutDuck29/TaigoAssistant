# order_handler.py

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from bot.keyboards import project_type_menu, minecraft_menu, software_menu, yes_no_menu, main_menu
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

@router.message(OrderState.waiting_for_category)
async def process_category(message: types.Message, state: FSMContext):
    category = message.text
    if category == "Сборка":
        await message.answer("📋 Введите название проекта:", reply_markup=types.ReplyKeyboardRemove())
        await state.update_data(category=category)
        await state.set_state(OrderState.waiting_for_name)
    else:
        await message.answer("Пожалуйста, выберите категорию.", reply_markup=minecraft_menu)

# Обработчик получения названия проекта
@router.message(OrderState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите версию проекта:")
    await state.set_state(OrderState.waiting_for_version)

# Обработчик получения версии проекта
@router.message(OrderState.waiting_for_version)
async def process_version(message: types.Message, state: FSMContext):
    await state.update_data(version=message.text)
    await message.answer("Укажите соц.сети проекта:")
    await state.set_state(OrderState.waiting_for_socials)

# Обработчик получения социальных сетей проекта
@router.message(OrderState.waiting_for_socials)
async def process_socials(message: types.Message, state: FSMContext):
    await state.update_data(socials=message.text)
    await message.answer("Нужен ли кастомный спавн?", reply_markup=yes_no_menu)
    await state.set_state(OrderState.waiting_for_spawn)

# Обработчик получения кастомного спавна
@router.message(OrderState.waiting_for_spawn)
async def process_spawn(message: types.Message, state: FSMContext):
    await state.update_data(spawn=message.text)
    await message.answer("Укажите желаемый срок выполнения проекта:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(OrderState.waiting_for_deadline)

# Обработчик получения срока выполнения проекта
@router.message(OrderState.waiting_for_deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    await state.update_data(deadline=message.text)
    user_data = await state.get_data()

    # Отправляем данные в группу
    if user_data["category"] == "Сборка":
        await bot.send_message(
            GROUP_ID,
            f"📢 Новый заказ!\n"
            f"🔹 {user_data['project_type']} | {user_data['category']}\n"
            f"🔹 Название: {user_data['name']}\n"
            f"🔹 Версия: {user_data['version']}\n"
            f"🔹 Соц.сети: {user_data['socials']}\n"
            f"🔹 Кастомный спавн: {user_data['spawn']}\n"
            f"🔹 Срок: {user_data['deadline']}\n"
            f"Заказчик: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
        )
        await message.answer("✅ Ваш заказ принят!", reply_markup=main_menu)

    await state.clear()

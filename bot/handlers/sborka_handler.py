# bot/order_handlers/build_handler.py

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from bot.keyboards import minecraft_menu, yes_no_menu, main_menu
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID

router = Router()

@router.message(OrderState.waiting_for_category)
async def process_build_category(message: types.Message, state: FSMContext):
    category = message.text
    if category == "Сборка":
        await message.answer("📋 Введите название проекта:", reply_markup=types.ReplyKeyboardRemove())
        await state.update_data(category=category)
        await state.set_state(OrderState.waiting_for_name)
    else:
        await message.answer("Пожалуйста, выберите категорию.", reply_markup=minecraft_menu)


@router.message(OrderState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите версию проекта:")
    await state.set_state(OrderState.waiting_for_version)

@router.message(OrderState.waiting_for_version)
async def process_version(message: types.Message, state: FSMContext):
    await state.update_data(version=message.text)
    await message.answer("Укажите соц.сети проекта:")
    await state.set_state(OrderState.waiting_for_socials)

@router.message(OrderState.waiting_for_socials)
async def process_socials(message: types.Message, state: FSMContext):
    await state.update_data(socials=message.text)
    await message.answer("Нужен ли кастомный спавн?", reply_markup=yes_no_menu)
    await state.set_state(OrderState.waiting_for_spawn)

@router.message(OrderState.waiting_for_spawn)
async def process_spawn(message: types.Message, state: FSMContext):
    await state.update_data(spawn=message.text)
    await message.answer("Укажите желаемый срок выполнения проекта:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(OrderState.waiting_for_deadline)

@router.message(OrderState.waiting_for_deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    await state.update_data(deadline=message.text)
    user_data = await state.get_data()

    if user_data["category"] == "Сборка":
        await bot.send_message(
            GROUP_ID,
            f"📢 Новый заказ на сборку!\n"
            f"🔹 {user_data['project_type']} | {user_data['category']}\n"
            f"🔹 Название: {user_data['name']}\n"
            f"🔹 Версия: {user_data['version']}\n"
            f"🔹 Соц.сети: {user_data['socials']}\n"
            f"🔹 Кастомный спавн: {user_data['spawn']}\n"
            f"🔹 Срок: {user_data['deadline']}\n"
            f"Заказчик: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
        )
        await message.answer("✅ Ваш заказ на сборку принят!", reply_markup=main_menu)

    await state.clear()

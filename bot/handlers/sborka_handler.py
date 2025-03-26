# bot/order_handlers/build_handler.py

from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.keyboards import minecraft_menu, yes_no_menu, main_menu, how_do_you_know_us, deadline
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID

router = Router()


@router.message(OrderState.waiting_for_category)
async def process_build_category(message: types.Message, state: FSMContext):
    category = message.text
    if category == "Сборка":
        await message.answer("📋 Введите название проекта:", reply_markup=ReplyKeyboardRemove())
        await state.update_data(category=category)
        await state.set_state(OrderState.waiting_for_name)
    else:
        await message.answer("Пожалуйста, выберите категорию.", reply_markup=minecraft_menu)


# Новый вопрос 1: Название проекта
@router.message(OrderState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите версию проекта:")
    await state.set_state(OrderState.waiting_for_version)


# Новый вопрос 2: Версия проекта
@router.message(OrderState.waiting_for_version)
async def process_version(message: types.Message, state: FSMContext):
    await state.update_data(version=message.text)
    await message.answer("Укажите соц.сети проекта:")
    await state.set_state(OrderState.waiting_for_socials)


# Новый вопрос 3: Социальные сети
@router.message(OrderState.waiting_for_socials)
async def process_socials(message: types.Message, state: FSMContext):
    await state.update_data(socials=message.text)
    await message.answer("Цветовая гамма Вашего проекта:")
    await state.set_state(OrderState.waiting_for_colors)


# Новый вопрос 4: Цветовая гамма
@router.message(OrderState.waiting_for_colors)
async def process_colors(message: types.Message, state: FSMContext):
    await state.update_data(colors=message.text)
    await message.answer("Тип режима (Анархия, БедВарс и т.д):")
    await state.set_state(OrderState.waiting_for_mode)


# Новый вопрос 5: Тип режима
@router.message(OrderState.waiting_for_mode)
async def process_mode(message: types.Message, state: FSMContext):
    await state.update_data(mode=message.text)
    await message.answer("Опишите функционал Вашего режима (в чем его смысл, и какие функции должны быть):")
    await state.set_state(OrderState.waiting_for_functionality)


# Новый вопрос 6: Описание функционала
@router.message(OrderState.waiting_for_functionality)
async def process_functionality(message: types.Message, state: FSMContext):
    await state.update_data(functionality=message.text)
    await message.answer("Нужен ли кастомный спавн? (Да/Нет)", reply_markup=yes_no_menu)
    await state.set_state(OrderState.waiting_for_spawn)


# Новый вопрос 7: Кастомный спавн
@router.message(OrderState.waiting_for_spawn)
async def process_spawn(message: types.Message, state: FSMContext):
    await state.update_data(spawn=message.text)
    await message.answer("Опишите, какие голограммы должны быть на сервере:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderState.waiting_for_holograms)


# Новый вопрос 8: Голограммы
@router.message(OrderState.waiting_for_holograms)
async def process_holograms(message: types.Message, state: FSMContext):
    await state.update_data(holograms=message.text)
    await message.answer("Есть ли необходимость в самописных решениях (плагинах)?", reply_markup=yes_no_menu)
    await state.set_state(OrderState.waiting_for_plugins)


# Новый вопрос 9: Самописные решения (плагины)
@router.message(OrderState.waiting_for_plugins)
async def process_plugins(message: types.Message, state: FSMContext):
    await state.update_data(plugins=message.text)
    await message.answer("Укажите, нужно ли создать самописный лаунчер под Ваш проект:", reply_markup=yes_no_menu)
    await state.set_state(OrderState.waiting_for_launcher)


# Новый вопрос 10: Самописный лаунчер
@router.message(OrderState.waiting_for_launcher)
async def process_launcher(message: types.Message, state: FSMContext):
    await state.update_data(launcher=message.text)
    await message.answer("Прикрепите иконку для Вашего проекта (ссылкой):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderState.waiting_for_icon)


# Новый вопрос 11: Иконка проекта
@router.message(OrderState.waiting_for_icon)
async def process_icon(message: types.Message, state: FSMContext):
    await state.update_data(icon=message.text)
    await message.answer("Нужен ли Вам сайт авто-доната (EasyDonate)?", reply_markup=yes_no_menu)
    await state.set_state(OrderState.waiting_for_donations)


# Новый вопрос 12: Сайт авто-доната
@router.message(OrderState.waiting_for_donations)
async def process_donations(message: types.Message, state: FSMContext):
    await state.update_data(donations=message.text)
    await message.answer("Здесь Вы можете описать что-то дополнительное, что было упущено в нашей форме на Ваш взгляд:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderState.waiting_for_additional)


# Новый вопрос 13: Дополнительное описание
@router.message(OrderState.waiting_for_additional)
async def process_additional(message: types.Message, state: FSMContext):
    await state.update_data(additional=message.text)
    await message.answer("Есть ли у Вас пожелания по поводу сроков?", reply_markup=deadline)
    await state.set_state(OrderState.waiting_for_deadline)


# Новый вопрос 14: Пожелания по срокам
@router.message(OrderState.waiting_for_deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    await state.update_data(deadline=message.text)
    await message.answer("Потребуется ли Вам в дальнейшем наша коммерческая поддержка?", reply_markup=yes_no_menu)
    await state.set_state(OrderState.waiting_for_support)


# Новый вопрос 15: Коммерческая поддержка
@router.message(OrderState.waiting_for_support)
async def process_support(message: types.Message, state: FSMContext):
    await state.update_data(support=message.text)
    await message.answer("Откуда Вы узнали о нашей студии?", reply_markup=how_do_you_know_us)
    await state.set_state(OrderState.waiting_for_source)


# Новый вопрос 16: Источник информации
@router.message(OrderState.waiting_for_source)
async def process_source(message: types.Message, state: FSMContext):
    await state.update_data(source=message.text)

    # После последнего вопроса отправим информацию в группу
    user_data = await state.get_data()

    await bot.send_message(
        GROUP_ID,
        f"📢 Новый заказ на сборку!\n"
        f"🔹 Название: {user_data['name']}\n"
        f"🔹 Версия: {user_data['version']}\n"
        f"🔹 Соц.сети: {user_data['socials']}\n"
        f"🔹 Цветовая гамма: {user_data['colors']}\n"
        f"🔹 Тип режима: {user_data['mode']}\n"
        f"🔹 Функционал: {user_data['functionality']}\n"
        f"🔹 Кастомный спавн: {user_data['spawn']}\n"
        f"🔹 Голограммы: {user_data['holograms']}\n"
        f"🔹 Плагины: {user_data['plugins']}\n"
        f"🔹 Лаунчер: {user_data['launcher']}\n"
        f"🔹 Иконка: {user_data['icon']}\n"
        f"🔹 Сайт авто-доната: {user_data['donations']}\n"
        f"🔹 Доп. описание: {user_data['additional']}\n"
        f"🔹 Сроки: {user_data['deadline']}\n"
        f"🔹 Коммерческая поддержка: {user_data['support']}\n"
        f"Заказчик: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
    )
    await message.answer("✅ Ваш заказ на сборку принят!", reply_markup=main_menu)

    await state.clear()
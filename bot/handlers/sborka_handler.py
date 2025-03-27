from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.keyboards import minecraft_menu, yes_no_menu, main_menu, how_do_you_know_us, deadline
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID

router = Router()

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
    await message.answer("Цветовая гамма Вашего проекта:")
    await state.set_state(OrderState.waiting_for_colors)


@router.message(OrderState.waiting_for_colors)
async def process_colors(message: types.Message, state: FSMContext):
    await state.update_data(colors=message.text)
    await message.answer("Тип режима (Анархия, БедВарс и т.д):")
    await state.set_state(OrderState.waiting_for_mode)


@router.message(OrderState.waiting_for_mode)
async def process_mode(message: types.Message, state: FSMContext):
    await state.update_data(mode=message.text)
    await message.answer("Опишите функционал Вашего режима (в чем его смысл, и какие функции должны быть):")
    await state.set_state(OrderState.waiting_for_functionality)


@router.message(OrderState.waiting_for_functionality)
async def process_functionality(message: types.Message, state: FSMContext):
    await state.update_data(functionality=message.text)
    await message.answer("Нужен ли кастомный спавн?", reply_markup=yes_no_menu)
    await state.set_state(OrderState.waiting_for_spawn)


@router.message(OrderState.waiting_for_spawn)
async def process_spawn(message: types.Message, state: FSMContext):
    await state.update_data(spawn=message.text)
    await message.answer("Опишите, какие голограммы должны быть на сервере:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderState.waiting_for_holograms)


@router.message(OrderState.waiting_for_holograms)
async def process_holograms(message: types.Message, state: FSMContext):
    await state.update_data(holograms=message.text)
    await message.answer("Есть ли необходимость в самописных решениях (плагинах)?", reply_markup=yes_no_menu)
    await state.set_state(OrderState.waiting_for_plugins)


@router.message(OrderState.waiting_for_plugins)
async def process_plugins(message: types.Message, state: FSMContext):
    await state.update_data(plugins=message.text)
    await message.answer("Укажите, нужно ли создать самописный лаунчер под Ваш проект:", reply_markup=yes_no_menu)
    await state.set_state(OrderState.waiting_for_launcher)


@router.message(OrderState.waiting_for_launcher)
async def process_launcher(message: types.Message, state: FSMContext):
    await state.update_data(launcher=message.text)
    await message.answer("Прикрепите иконку для Вашего проекта (ссылкой):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderState.waiting_for_icon)


@router.message(OrderState.waiting_for_icon)
async def process_icon(message: types.Message, state: FSMContext):
    await state.update_data(icon=message.text)
    await message.answer("Нужен ли Вам сайт авто-доната (EasyDonate)?", reply_markup=yes_no_menu)
    await state.set_state(OrderState.waiting_for_donations)


@router.message(OrderState.waiting_for_donations)
async def process_donations(message: types.Message, state: FSMContext):
    await state.update_data(donations=message.text)
    await message.answer("Здесь Вы можете описать что-то дополнительное, что было упущено в нашей форме на Ваш взгляд:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderState.waiting_for_additional)


@router.message(OrderState.waiting_for_additional)
async def process_additional(message: types.Message, state: FSMContext):
    await state.update_data(additional=message.text)
    await message.answer("Есть ли у Вас пожелания по поводу сроков?", reply_markup=deadline)
    await state.set_state(OrderState.waiting_for_deadline)


@router.message(OrderState.waiting_for_deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    await state.update_data(deadline=message.text)
    await message.answer("Потребуется ли Вам в дальнейшем наша коммерческая поддержка?", reply_markup=yes_no_menu)
    await state.set_state(OrderState.waiting_for_support)


@router.message(OrderState.waiting_for_support)
async def process_support(message: types.Message, state: FSMContext):
    await state.update_data(support=message.text)
    await message.answer("Откуда Вы узнали о нашей студии?", reply_markup=how_do_you_know_us)
    await state.set_state(OrderState.waiting_for_source)


@router.message(OrderState.waiting_for_source)
async def process_source(message: types.Message, state: FSMContext):
    await state.update_data(source=message.text)

    user_data = await state.get_data()

    await bot.send_message(
        GROUP_ID,
        f"📢 Новый заказ на сборку!\n\n"
        f"🔹 Название:\n — {user_data['name']}\n"
        f"🔹 Версия:\n — {user_data['version']}\n"
        f"🔹 Соц.сети:\n — {user_data['socials']}\n"
        f"🔹 Цветовая гамма:\n — {user_data['colors']}\n"
        f"🔹 Тип режима:\n — {user_data['mode']}\n"
        f"🔹 Функционал:\n — {user_data['functionality']}\n"
        f"🔹 Кастомный спавн:\n — {user_data['spawn']}\n"
        f"🔹 Голограммы:\n — {user_data['holograms']}\n"
        f"🔹 Плагины:\n — {user_data['plugins']}\n"
        f"🔹 Лаунчер:\n — {user_data['launcher']}\n"
        f"🔹 Иконка:\n — {user_data['icon']}\n"
        f"🔹 Сайт авто-доната:\n — {user_data['donations']}\n"
        f"🔹 Доп. описание:\n — {user_data['additional']}\n"
        f"🔹 Сроки:\n — {user_data['deadline']}\n"
        f"🔹 Коммерческая поддержка:\n — {user_data['support']}\n\n"
        f"Заказчик: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
    )
    await message.answer("✅ Ваш заказ на сборку принят!", reply_markup=main_menu)

    await state.clear()
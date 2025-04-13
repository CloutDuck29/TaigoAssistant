from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.keyboards import minecraft_menu, yes_no_menu, main_menu, how_do_you_know_us, deadline
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID
from aiogram.filters import Command

router = Router()

order_build_steps = {
    'name': {"question": "Введите версию проекта", "next_state": OrderState.waiting_for_version},
    'version': {"question": "Укажите соц.сети проекта", "next_state": OrderState.waiting_for_socials},
    'socials': {"question": "Цветовая гамма Вашего проекта", "next_state": OrderState.waiting_for_colors},
    'colors': {"question": "Тип режима (Анархия, БедВарс и т.д)", "next_state": OrderState.waiting_for_mode},
    'mode': {"question": "Опишите функционал Вашего режима (в чем его смысл, и какие функции должны быть)",
             "next_state": OrderState.waiting_for_functionality},
    'functionality': {"question": "Нужен ли кастомный спавн?", "next_state": OrderState.waiting_for_spawn, "keyboard": yes_no_menu},
    'spawn': {"question": "Опишите, какие голограммы должны быть на сервере", "next_state": OrderState.waiting_for_holograms},
    'holograms': {"question": "Есть ли необходимость в самописных решениях (плагинах)?", "next_state": OrderState.waiting_for_plugins, "keyboard": yes_no_menu},
    'plugins': {"question": "Укажите, нужно ли создать самописный лаунчер под Ваш проект", "next_state": OrderState.waiting_for_launcher, "keyboard": yes_no_menu},
    'launcher': {"question": "Прикрепите иконку для Вашего проекта (ссылкой)", "next_state": OrderState.waiting_for_icon},
    'icon': {"question": "Нужен ли Вам сайт авто-доната (EasyDonate)?", "next_state": OrderState.waiting_for_donations, "keyboard": yes_no_menu},
    'donations': {"question": "Здесь Вы можете описать что-то дополнительное, что было упущено в нашей форме на Ваш взгляд",
                  "next_state": OrderState.waiting_for_additional},
    'additional': {"question": "Есть ли у Вас пожелания по поводу сроков?", "next_state": OrderState.waiting_for_deadline, "keyboard": deadline},
    'deadline': {"question": "Потребуется ли Вам в дальнейшем наша коммерческая поддержка?", "next_state": OrderState.waiting_for_support, "keyboard": yes_no_menu},
    'support': {"question": "Откуда Вы узнали о нашей студии?", "next_state": OrderState.waiting_for_source, "keyboard": how_do_you_know_us},
    'source': {"question": None, "next_state": None}
}

async def process_order_build_step(message: types.Message, state: FSMContext, field: str):
    # Проверка на команду /cancel на каждом шаге
    if message.text.lower() == "/cancel":
        await state.clear()
        await message.answer("🚫 Заказ отменён. Вы вернулись в главное меню.", reply_markup=main_menu)
        return

    await state.update_data({field: message.text})

    step_info = order_build_steps[field]
    if step_info["question"]:
        text = step_info["question"]

        if field == "name":
            text += "\n\n❗ Если хотите отменить заказ — введите /cancel"

        await message.answer(text, reply_markup=step_info.get("keyboard", ReplyKeyboardRemove()))

    if step_info["next_state"]:
        await state.set_state(step_info["next_state"])
    else:
        await complete_build_order(message, state)

async def complete_build_order(message: types.Message, state: FSMContext):
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
        f"🔹 Коммерческая поддержка:\n — {user_data['support']}\n"
        f"🔹 Откуда узнали:\n — {user_data['source']}\n\n"
        f"Заказчик: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
    )
    await message.answer("✅ Ваш заказ на сборку принят!", reply_markup=main_menu)
    await state.clear()

# Хендлер для отмены
@router.message(Command("cancel"))
async def cancel_order_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🚫 Заказ отменён. Вы вернулись в главное меню.", reply_markup=main_menu)


# Хендлеры для обработки шагов заказа
@router.message(OrderState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'name')


@router.message(OrderState.waiting_for_version)
async def process_version(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'version')


@router.message(OrderState.waiting_for_socials)
async def process_socials(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'socials')


@router.message(OrderState.waiting_for_colors)
async def process_colors(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'colors')


@router.message(OrderState.waiting_for_mode)
async def process_mode(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'mode')


@router.message(OrderState.waiting_for_functionality)
async def process_functionality(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'functionality')


@router.message(OrderState.waiting_for_spawn)
async def process_spawn(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'spawn')


@router.message(OrderState.waiting_for_holograms)
async def process_holograms(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'holograms')


@router.message(OrderState.waiting_for_plugins)
async def process_plugins(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'plugins')


@router.message(OrderState.waiting_for_launcher)
async def process_launcher(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'launcher')


@router.message(OrderState.waiting_for_icon)
async def process_icon(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'icon')


@router.message(OrderState.waiting_for_donations)
async def process_donations(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'donations')


@router.message(OrderState.waiting_for_additional)
async def process_additional(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'additional')


@router.message(OrderState.waiting_for_deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'deadline')


@router.message(OrderState.waiting_for_support)
async def process_support(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'support')


@router.message(OrderState.waiting_for_source)
async def process_source(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'source')

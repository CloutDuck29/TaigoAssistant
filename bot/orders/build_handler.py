from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from bot.keyboards import minecraft_menu, yes_no_menu, main_menu, how_do_you_know_us, deadline
from bot.states import OrderState
from bot.loader import bot
from aiogram.types import ReplyKeyboardRemove
from bot.config import GROUP_ID
from aiogram.filters import Command


router = Router()

order_steps = {
    'type': {"question": "Укажите версию, на которой необходимо строить",
             "next_state": OrderState.waiting_for_versionBuild},
    'version': {"question": "Опишите, что именно Вы хотите видеть в постройке",
                "next_state": OrderState.waiting_for_whatToBuild},
    'build': {"question": "Укажите стиль постройки (хай-тек, модерн, и т.д)",
              "next_state": OrderState.waiting_for_styleOfBuild},
    'style': {"question": "Укажите размерность Вашей постройки (в блоках, например 150х150)",
              "next_state": OrderState.waiting_for_sizeOfBuild},
    'size': {"question": "Укажите уровень детализации проекта (низкий, средний, высокий)",
             "next_state": OrderState.waiting_for_detalizationOfBuild},
    'detalization': {"question": "Укажите сезон постройки (если он имеет место быть)",
                     "next_state": OrderState.waiting_for_sezonOfBuild},
    'sezon': {"question": "Нужно ли расставлять точки для определенных локаций (укажите, где и сколько)",
              "next_state": OrderState.waiting_for_pointsOfBuild},
    'points': {
        "question": "Предоставьте картинки построек наподобие, как примеры, на которые мы могли бы ориентироваться",
        "next_state": OrderState.waiting_for_picturesOfBuild},
    'pictures': {
        "question": "Здесь Вы можете описать что-то дополнительное, что было упущено в нашей форме на Ваш взгляд, необходимое Вашему проекту",
        "next_state": OrderState.waiting_for_extraInfoBuild},
    'extra': {"question": "Есть ли у Вас пожелания по поводу сроков?",
              "next_state": OrderState.waiting_for_deadlineBuild, "keyboard": deadline},
    'deadline': {"question": "Откуда Вы узнали о нас?", "next_state": OrderState.waiting_for_sourceBuild,
                 "keyboard": how_do_you_know_us},
    'source': {"question": None, "next_state": None}
}


async def process_order_step(message: types.Message, state: FSMContext, field: str):
    await state.update_data({field: message.text})

    step_info = order_steps[field]

    if step_info["question"]:
        text = step_info["question"]

        if field == "type":
            text += "\n\n❗ Если хотите отменить заказ — введите /cancel"

        await message.answer(text, reply_markup=step_info.get("keyboard", ReplyKeyboardRemove()))

    if step_info["next_state"]:
        await state.set_state(step_info["next_state"])
    else:
        await complete_order(message, state)


async def complete_order(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.send_message(
        GROUP_ID,
        f"📢 Новый заказ на постройку!\n\n"
        f"🔹 Тип постройки:\n — {user_data['type']}\n"
        f"🔹 Версия:\n — {user_data['version']}\n"
        f"🔹 Что нужно построить:\n — {user_data['build']}\n"
        f"🔹 Стиль постройки:\n — {user_data['style']}\n"
        f"🔹 Размер постройки:\n — {user_data['size']}\n"
        f"🔹 Уровень детализации:\n — {user_data['detalization']}\n"
        f"🔹 Сезон постройки:\n — {user_data['sezon']}\n"
        f"🔹 Точки локаций:\n — {user_data['points']}\n"
        f"🔹 Примеры:\n — {user_data['pictures']}\n"
        f"🔹 Дополнительная информация:\n — {user_data['extra']}\n"
        f"🔹 Сроки:\n — {user_data['deadline']}\n"
        f"🔹 Откуда Вы узнали о нас:\n — {user_data['source']}\n\n"
        f"Заказчик: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
    )
    await message.answer("✅ Ваш заказ на постройку принят!", reply_markup=main_menu)
    await state.clear()

@router.message(Command("cancel"))
async def cancel_order_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🚫 Заказ отменён. Вы вернулись в главное меню.", reply_markup=main_menu)


@router.message(OrderState.waiting_for_typeBuild)
async def process_type_build(message: types.Message, state: FSMContext):
    await process_order_step(message, state, 'type')


@router.message(OrderState.waiting_for_versionBuild)
async def process_version(message: types.Message, state: FSMContext):
    await process_order_step(message, state, 'version')


@router.message(OrderState.waiting_for_whatToBuild)
async def process_whattobuild(message: types.Message, state: FSMContext):
    await process_order_step(message, state, 'build')


@router.message(OrderState.waiting_for_styleOfBuild)
async def process_style(message: types.Message, state: FSMContext):
    await process_order_step(message, state, 'style')


@router.message(OrderState.waiting_for_sizeOfBuild)
async def process_size(message: types.Message, state: FSMContext):
    await process_order_step(message, state, 'size')


@router.message(OrderState.waiting_for_detalizationOfBuild)
async def process_detalization(message: types.Message, state: FSMContext):
    await process_order_step(message, state, 'detalization')


@router.message(OrderState.waiting_for_sezonOfBuild)
async def process_sezon(message: types.Message, state: FSMContext):
    await process_order_step(message, state, 'sezon')


@router.message(OrderState.waiting_for_pointsOfBuild)
async def process_points(message: types.Message, state: FSMContext):
    await process_order_step(message, state, 'points')


@router.message(OrderState.waiting_for_picturesOfBuild)
async def process_pictures(message: types.Message, state: FSMContext):
    await process_order_step(message, state, 'pictures')


@router.message(OrderState.waiting_for_extraInfoBuild)
async def process_extra(message: types.Message, state: FSMContext):
    await process_order_step(message, state, 'extra')


@router.message(OrderState.waiting_for_deadlineBuild)
async def process_deadline(message: types.Message, state: FSMContext):
    await process_order_step(message, state, 'deadline')


@router.message(OrderState.waiting_for_sourceBuild)
async def process_source_build(message: types.Message, state: FSMContext):
    await process_order_step(message, state, 'source')






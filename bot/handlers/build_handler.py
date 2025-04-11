from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.keyboards import minecraft_menu, yes_no_menu, main_menu, how_do_you_know_us, deadline
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID

router = Router()

@router.message(OrderState.waiting_for_typeBuild)
async def process_type_build(message: types.Message, state: FSMContext):
    await state.update_data(type=message.text)
    await message.answer("Укажите версию, на которой необходимо строить")
    await state.set_state(OrderState.waiting_for_versionBuild)

@router.message(OrderState.waiting_for_versionBuild)
async def process_version(message: types.Message, state: FSMContext):
    await state.update_data(version=message.text)
    await message.answer("Опишите, что именно Вы хотите видеть в постройке")
    await state.set_state(OrderState.waiting_for_whatToBuild)

@router.message(OrderState.waiting_for_whatToBuild)
async def process_whattobuild(message: types.Message, state: FSMContext):
    await state.update_data(build=message.text)
    await message.answer("Укажите стиль постройки (хай-тек, модерн, и т.д)")
    await state.set_state(OrderState.waiting_for_styleOfBuild)

@router.message(OrderState.waiting_for_styleOfBuild)
async def process_style(message: types.Message, state: FSMContext):
    await state.update_data(style=message.text)
    await message.answer("Укажите размерность Вашей постройки (в блоках, например 150х150)")
    await state.set_state(OrderState.waiting_for_sizeOfBuild)


@router.message(OrderState.waiting_for_sizeOfBuild)
async def process_size(message: types.Message, state: FSMContext):
    await state.update_data(size=message.text)
    await message.answer("Укажите уровень детализации проекта (низкий, средний, высокий)")
    await state.set_state(OrderState.waiting_for_detalizationOfBuild)

@router.message(OrderState.waiting_for_detalizationOfBuild)
async def process_detalization(message: types.Message, state: FSMContext):
    await state.update_data(detalization=message.text)
    await message.answer("Укажите сезон постройки (если он имеет место быть)")
    await state.set_state(OrderState.waiting_for_sezonOfBuild)

@router.message(OrderState.waiting_for_sezonOfBuild)
async def process_sezon(message: types.Message, state: FSMContext):
    await state.update_data(sezon=message.text)
    await message.answer("Нужно ли расставлять точки для определенных локаций (укажите, где и сколько)")
    await state.set_state(OrderState.waiting_for_pointsOfBuild)


@router.message(OrderState.waiting_for_pointsOfBuild)
async def process_points(message: types.Message, state: FSMContext):
    await state.update_data(points=message.text)
    await message.answer("Предоставьте картинки построек наподобие, как примеры, на которые мы могли бы ориентироваться")
    await state.set_state(OrderState.waiting_for_picturesOfBuild)

@router.message(OrderState.waiting_for_picturesOfBuild)
async def process_pictures(message: types.Message, state: FSMContext):
    await state.update_data(pictures=message.text)
    await message.answer("Здесь Вы можете описать что-то дополнительное, что было упущено в нашей форме на Ваш взгляд, необходимое Вашему проекту")
    await state.set_state(OrderState.waiting_for_extraInfoBuild)

@router.message(OrderState.waiting_for_extraInfoBuild)
async def process_extra(message: types.Message, state: FSMContext):
    await state.update_data(extra=message.text)
    await message.answer("Есть ли у Вас пожелания по поводу сроков?", reply_markup=deadline)
    await state.set_state(OrderState.waiting_for_deadlineBuild)

@router.message(OrderState.waiting_for_deadlineBuild)
async def process_deadline(message: types.Message, state: FSMContext):
    await state.update_data(deadline=message.text)
    await message.answer("Откуда Вы узнали о нас?", reply_markup= how_do_you_know_us)
    await state.set_state(OrderState.waiting_for_sourceBuild)

@router.message(OrderState.waiting_for_sourceBuild)
async def process_source_build(message: types.Message, state: FSMContext):
    await state.update_data(source=message.text)

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
        f"🔹 Откуда Вы узнали о нас:\n — {user_data['source']}\n"

        f"Заказчик: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
    )
    await message.answer("✅ Ваш заказ на постройку принят!", reply_markup=main_menu)

    await state.clear()

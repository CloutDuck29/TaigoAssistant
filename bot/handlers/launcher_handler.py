from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.keyboards import minecraft_menu, yes_no_menu, main_menu, how_do_you_know_us, deadline
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID

router = Router()

@router.message(OrderState.waiting_for_nameLauncher)
async def process_name_launcher(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите версию лаунчера:")
    await state.set_state(OrderState.waiting_for_versionLauncher)

@router.message(OrderState.waiting_for_versionLauncher)
async def process_version(message: types.Message, state: FSMContext):
    await state.update_data(version=message.text)
    await message.answer("Укажите функционал лаунчера и какие задачи он должен решать:")
    await state.set_state(OrderState.waiting_for_funcLauncher)

@router.message(OrderState.waiting_for_funcLauncher)
async def process_func(message: types.Message, state: FSMContext):
    await state.update_data(func=message.text)
    await message.answer("Укажите, есть ли вспомогательные системы, с которыми должен работать лаунчер (библиотеки, какие-то смежные плагины):")
    await state.set_state(OrderState.waiting_for_addonsLauncher)

@router.message(OrderState.waiting_for_addonsLauncher)
async def process_addons(message: types.Message, state: FSMContext):
    await state.update_data(addons=message.text)
    await message.answer("Предоставьте примеры лаунчеров наподобие, на которые мы могли бы ориентироваться (при наличии)")
    await state.set_state(OrderState.waiting_for_examplesLauncher)


@router.message(OrderState.waiting_for_examplesLauncher)
async def process_examples(message: types.Message, state: FSMContext):
    await state.update_data(examples=message.text)
    await message.answer("Здесь Вы можете описать что-то дополнительное, что было упущено в нашей форме на Ваш взгляд, необходимое Вашему проекту")
    await state.set_state(OrderState.waiting_for_extraInfoLauncher)


@router.message(OrderState.waiting_for_extraInfoLauncher)
async def process_extra(message: types.Message, state: FSMContext):
    await state.update_data(extra=message.text)
    await message.answer("Есть ли у Вас пожелания по поводу сроков?", reply_markup=deadline)
    await state.set_state(OrderState.waiting_for_deadlineLauncher)


@router.message(OrderState.waiting_for_deadlineLauncher)
async def process_dead(message: types.Message, state: FSMContext):
    await state.update_data(dead=message.text)
    await message.answer("Откуда Вы узнали о нашей студии?", reply_markup=how_do_you_know_us)
    await state.set_state(OrderState.waiting_for_sourceLauncher)


@router.message(OrderState.waiting_for_sourceLauncher)
async def process_source_launcher(message: types.Message, state: FSMContext):
    await state.update_data(source=message.text)

    user_data = await state.get_data()

    await bot.send_message(
        GROUP_ID,
        f"📢 1Новый заказ на плагин!\n\n"
        f"🔹 Название:\n — {user_data['name']}\n"
        f"🔹 Версия и ядро:\n — {user_data['version']}\n"
        f"🔹 Функционал лаунчера:\n — {user_data['func']}\n"
        f"🔹 Вспомогательные системы:\n — {user_data['addons']}\n"
        f"🔹 Примеры:\n — {user_data['examples']}\n"
        f"🔹 Дополнительная информация:\n — {user_data['extra']}\n"
        f"🔹 Сроки:\n — {user_data['dead']}\n"
        f"🔹 Откуда узнали о нас:\n — {user_data['source']}\n"
        f"Заказчик: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
    )
    await message.answer("✅ Ваш заказ на лаунчер принят!", reply_markup=main_menu)

    await state.clear()

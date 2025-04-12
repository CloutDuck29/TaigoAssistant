from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.keyboards import minecraft_menu, yes_no_menu, main_menu, how_do_you_know_us, deadline
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID

router = Router()

@router.message(OrderState.waiting_for_namePlugin)
async def process_name_plugin(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ядро плагина")
    await state.set_state(OrderState.waiting_for_jarPlugin)

@router.message(OrderState.waiting_for_jarPlugin)
async def process_version(message: types.Message, state: FSMContext):
    await state.update_data(jar=message.text)
    await message.answer("Укажите версию плагина")
    await state.set_state(OrderState.waiting_for_versionPlugin)

@router.message(OrderState.waiting_for_versionPlugin)
async def process_socials(message: types.Message, state: FSMContext):
    await state.update_data(version=message.text)
    await message.answer("Укажите функционал плагина и какие задачи он должен решать")
    await state.set_state(OrderState.waiting_for_funcPlugin)

@router.message(OrderState.waiting_for_funcPlugin)
async def process_colors(message: types.Message, state: FSMContext):
    await state.update_data(functional=message.text)
    await message.answer("Укажите, есть ли вспомогательные системы, с которыми должен работать плагин (библиотеки, какие-то смежные плагины)")
    await state.set_state(OrderState.waiting_for_addonsPlugin)


@router.message(OrderState.waiting_for_addonsPlugin)
async def process_mode(message: types.Message, state: FSMContext):
    await state.update_data(addons=message.text)
    await message.answer("Предоставьте примеры плагины с функционалом наподобие, на которые мы могли бы ориентироваться (при наличии)")
    await state.set_state(OrderState.waiting_for_examplesPlugin)


@router.message(OrderState.waiting_for_examplesPlugin)
async def process_functionality(message: types.Message, state: FSMContext):
    await state.update_data(examples=message.text)
    await message.answer("Здесь Вы можете описать что-то дополнительное, что было упущено в нашей форме на Ваш взгляд, необходимое Вашему проекту")
    await state.set_state(OrderState.waiting_for_extraInfoPlugin)


@router.message(OrderState.waiting_for_extraInfoPlugin)
async def process_spawn(message: types.Message, state: FSMContext):
    await state.update_data(extrainfo=message.text)
    await message.answer("Есть ли у Вас пожелания по поводу сроков?", reply_markup=deadline)
    await state.set_state(OrderState.waiting_for_deadlinePlugin)


@router.message(OrderState.waiting_for_deadlinePlugin)
async def process_holograms(message: types.Message, state: FSMContext):
    await state.update_data(deadlines=message.text)
    await message.answer("Откуда Вы узнали о нашей студии?", reply_markup=how_do_you_know_us)
    await state.set_state(OrderState.waiting_for_sourcePlugin)



@router.message(OrderState.waiting_for_sourcePlugin)
async def process_source_plugin(message: types.Message, state: FSMContext):
    await state.update_data(source=message.text)

    user_data = await state.get_data()

    await bot.send_message(
        GROUP_ID,
        f"📢 Новый заказ на плагин!\n\n"
        f"🔸 Название:\n — {user_data['name']}\n"
        f"🔸 Ядро:\n — {user_data['jar']}\n"
        f"🔸 Версия:\n — {user_data['version']}\n"
        f"🔸 Функционал и задачи плагина:\n — {user_data['functional']}\n"
        f"🔸 Вспомогательные системы/библиотеки:\n — {user_data['addons']}\n"
        f"🔸 Примеры:\n — {user_data['examples']}\n"
        f"🔸 Дополнительная информация:\n — {user_data['extrainfo']}\n"
        f"🔸 Сроки:\n — {user_data['deadlines']}\n"
        f"🔸 Откуда узнали о нас:\n — {user_data['source']}\n\n"
        f"Заказчик: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
    )
    await message.answer("✅ Ваш заказ на плагин принят!", reply_markup=main_menu)

    await state.clear()
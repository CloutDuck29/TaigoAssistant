from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.keyboards import minecraft_menu, yes_no_menu, main_menu, how_do_you_know_us, deadline
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID

router = Router()

order_plugin_steps = {
    'name': {"question": "Введите ядро плагина", "next_state": OrderState.waiting_for_jarPlugin},
    'jar': {"question": "Укажите версию плагина", "next_state": OrderState.waiting_for_versionPlugin},
    'version': {"question": "Укажите функционал плагина и какие задачи он должен решать",
                "next_state": OrderState.waiting_for_funcPlugin},
    'functional': {"question": "Укажите, есть ли вспомогательные системы, с которыми должен работать плагин (библиотеки, какие-то смежные плагины)",
                   "next_state": OrderState.waiting_for_addonsPlugin},
    'addons': {"question": "Предоставьте примеры плагинов с функционалом наподобие, на которые мы могли бы ориентироваться (при наличии)",
               "next_state": OrderState.waiting_for_examplesPlugin},
    'examples': {"question": "Здесь Вы можете описать что-то дополнительное, что было упущено в нашей форме на Ваш взгляд, необходимое Вашему проекту",
                 "next_state": OrderState.waiting_for_extraInfoPlugin},
    'extrainfo': {"question": "Есть ли у Вас пожелания по поводу сроков?", "next_state": OrderState.waiting_for_deadlinePlugin,
                  "keyboard": deadline},
    'deadlines': {"question": "Откуда Вы узнали о нашей студии?", "next_state": OrderState.waiting_for_sourcePlugin,
                  "keyboard": how_do_you_know_us},
    'source': {"question": None, "next_state": None}
}


async def process_order_plugin_step(message: types.Message, state: FSMContext, field: str):
    await state.update_data({field: message.text})

    step_info = order_plugin_steps[field]
    if step_info["question"]:
        await message.answer(step_info["question"], reply_markup=step_info.get("keyboard", ReplyKeyboardRemove()))

    if step_info["next_state"]:
        await state.set_state(step_info["next_state"])
    else:
        await complete_plugin_order(message, state)


async def complete_plugin_order(message: types.Message, state: FSMContext):
    """Завершаем заказ на плагин и отправляем информацию в группу."""
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


@router.message(OrderState.waiting_for_namePlugin)
async def process_name_plugin(message: types.Message, state: FSMContext):
    await process_order_plugin_step(message, state, 'name')


@router.message(OrderState.waiting_for_jarPlugin)
async def process_jar_plugin(message: types.Message, state: FSMContext):
    await process_order_plugin_step(message, state, 'jar')


@router.message(OrderState.waiting_for_versionPlugin)
async def process_version_plugin(message: types.Message, state: FSMContext):
    await process_order_plugin_step(message, state, 'version')


@router.message(OrderState.waiting_for_funcPlugin)
async def process_func_plugin(message: types.Message, state: FSMContext):
    await process_order_plugin_step(message, state, 'functional')


@router.message(OrderState.waiting_for_addonsPlugin)
async def process_addons_plugin(message: types.Message, state: FSMContext):
    await process_order_plugin_step(message, state, 'addons')


@router.message(OrderState.waiting_for_examplesPlugin)
async def process_examples_plugin(message: types.Message, state: FSMContext):
    await process_order_plugin_step(message, state, 'examples')


@router.message(OrderState.waiting_for_extraInfoPlugin)
async def process_extra_plugin(message: types.Message, state: FSMContext):
    await process_order_plugin_step(message, state, 'extrainfo')


@router.message(OrderState.waiting_for_deadlinePlugin)
async def process_deadline_plugin(message: types.Message, state: FSMContext):
    await process_order_plugin_step(message, state, 'deadlines')


@router.message(OrderState.waiting_for_sourcePlugin)
async def process_source_plugin(message: types.Message, state: FSMContext):
    await process_order_plugin_step(message, state, 'source')

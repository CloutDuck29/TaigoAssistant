from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.keyboards import minecraft_menu, yes_no_menu, main_menu, how_do_you_know_us, deadline
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID

router = Router()

order_launcher_steps = {
    'name': {"question": "Введите версию лаунчера", "next_state": OrderState.waiting_for_versionLauncher},
    'version': {"question": "Укажите функционал лаунчера и какие задачи он должен решать",
                "next_state": OrderState.waiting_for_funcLauncher},
    'func': {"question": "Укажите, есть ли вспомогательные системы, с которыми должен работать лаунчер (библиотеки, какие-то смежные плагины)",
             "next_state": OrderState.waiting_for_addonsLauncher},
    'addons': {"question": "Предоставьте примеры лаунчеров наподобие, на которые мы могли бы ориентироваться (при наличии)",
               "next_state": OrderState.waiting_for_examplesLauncher},
    'examples': {"question": "Здесь Вы можете описать что-то дополнительное, что было упущено в нашей форме на Ваш взгляд, необходимое Вашему проекту",
                 "next_state": OrderState.waiting_for_designLauncher},
    'extra': {"question": "Предоставьте ссылку на дизайн (если имеется) или укажите, что дизайн нужно разработать",
              "next_state": OrderState.waiting_for_extraInfoLauncher},
    'design': {"question": "Есть ли у Вас пожелания по поводу сроков?", "next_state": OrderState.waiting_for_deadlineLauncher,
               "keyboard": deadline},
    'dead': {"question": "Откуда Вы узнали о нашей студии?", "next_state": OrderState.waiting_for_sourceLauncher,
             "keyboard": how_do_you_know_us},
    'source': {"question": None, "next_state": None}
}


async def process_order_launcher_step(message: types.Message, state: FSMContext, field: str):
    await state.update_data({field: message.text})

    step_info = order_launcher_steps[field]
    if step_info["question"]:
        await message.answer(step_info["question"], reply_markup=step_info.get("keyboard", ReplyKeyboardRemove()))

    if step_info["next_state"]:
        await state.set_state(step_info["next_state"])
    else:
        await complete_launcher_order(message, state)


async def complete_launcher_order(message: types.Message, state: FSMContext):
    """Завершаем заказ на лаунчер и отправляем информацию в группу."""
    user_data = await state.get_data()
    await bot.send_message(
        GROUP_ID,
        f"📢 Новый заказ на лаунчер!\n\n"
        f"♦️ Название:\n — {user_data['name']}\n"
        f"♦️ Версия:\n — {user_data['version']}\n"
        f"♦️ Функционал лаунчера:\n — {user_data['func']}\n"
        f"♦️ Вспомогательные системы:\n — {user_data['addons']}\n"
        f"♦️ Примеры:\n — {user_data['examples']}\n"
        f"♦️ Дополнительная информация:\n — {user_data['extra']}\n"
        f"♦️ Дизайн:\n — {user_data['design']}\n"
        f"♦️ Сроки:\n — {user_data['dead']}\n"
        f"♦️ Откуда узнали о нас:\n — {user_data['source']}\n\n"
        f"Заказчик: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
    )
    await message.answer("✅ Ваш заказ на лаунчер принят!", reply_markup=main_menu)
    await state.clear()


@router.message(OrderState.waiting_for_nameLauncher)
async def process_name_launcher(message: types.Message, state: FSMContext):
    await process_order_launcher_step(message, state, 'name')


@router.message(OrderState.waiting_for_versionLauncher)
async def process_version_launcher(message: types.Message, state: FSMContext):
    await process_order_launcher_step(message, state, 'version')


@router.message(OrderState.waiting_for_funcLauncher)
async def process_func_launcher(message: types.Message, state: FSMContext):
    await process_order_launcher_step(message, state, 'func')


@router.message(OrderState.waiting_for_addonsLauncher)
async def process_addons_launcher(message: types.Message, state: FSMContext):
    await process_order_launcher_step(message, state, 'addons')


@router.message(OrderState.waiting_for_examplesLauncher)
async def process_examples_launcher(message: types.Message, state: FSMContext):
    await process_order_launcher_step(message, state, 'examples')


@router.message(OrderState.waiting_for_designLauncher)
async def process_design_launcher(message: types.Message, state: FSMContext):
    await process_order_launcher_step(message, state, 'extra')


@router.message(OrderState.waiting_for_extraInfoLauncher)
async def process_extra_launcher(message: types.Message, state: FSMContext):
    await process_order_launcher_step(message, state, 'design')


@router.message(OrderState.waiting_for_deadlineLauncher)
async def process_deadline_launcher(message: types.Message, state: FSMContext):
    await process_order_launcher_step(message, state, 'dead')


@router.message(OrderState.waiting_for_sourceLauncher)
async def process_source_launcher(message: types.Message, state: FSMContext):
    await process_order_launcher_step(message, state, 'source')

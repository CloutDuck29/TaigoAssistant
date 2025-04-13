from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.keyboards import minecraft_menu, yes_no_menu, main_menu, how_do_you_know_us, deadline
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID
from aiogram.filters import Command

router = Router()

order_site_steps = {
    'name': {"question": "Укажите свой домен (при наличии)", "next_state": OrderState.waiting_for_siteDomain},
    'domain': {"question": "Укажите какие страницы должны быть на сайте и их описание",
               "next_state": OrderState.waiting_for_layoutSite},
    'layout': {"question": "Укажите функционал сайта и какие задачи он должен решать",
               "next_state": OrderState.waiting_for_funcSite},
    'func': {"question": "Укажите, есть ли вспомогательные системы, с которыми должен работать сайт",
             "next_state": OrderState.waiting_for_addonsSite},
    'addons': {
        "question": "Предоставьте примеры сайтов наподобие, на которые мы могли бы ориентироваться (при наличии)",
        "next_state": OrderState.waiting_for_examplesSite},
    'examples': {"question": "Предоставьте ссылку на дизайн (при наличии)",
                 "next_state": OrderState.waiting_for_designSite},
    'design': {
        "question": "Здесь Вы можете описать что-то дополнительное, что было упущено в нашей форме на Ваш взгляд, необходимое Вашему проекту",
        "next_state": OrderState.waiting_for_extraInfoSite},
    'extra': {"question": "Есть ли у Вас пожелания по поводу сроков?",
              "next_state": OrderState.waiting_for_deadlineSite, "keyboard": deadline},
    'dead': {"question": "Откуда Вы узнали о нашей студии?", "next_state": OrderState.waiting_for_sourceSite,
             "keyboard": how_do_you_know_us},
    'source': {"question": None, "next_state": None}
}

async def process_order_site_step(message: types.Message, state: FSMContext, field: str):
    if message.text.lower() == "/cancel":
        await state.clear()
        await message.answer("🚫 Заказ отменён. Вы вернулись в главное меню.", reply_markup=main_menu)
        return

    await state.update_data({field: message.text})

    step_info = order_site_steps[field]
    if step_info["question"]:
        text = step_info["question"]
        if field == "name":
            text += "\n\n❗ Если хотите отменить заказ — введите /cancel"

        await message.answer(text, reply_markup=step_info.get("keyboard", ReplyKeyboardRemove()))

    if step_info["next_state"]:
        await state.set_state(step_info["next_state"])
    else:
        await complete_site_order(message, state)


async def complete_site_order(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    full_text = (
        f"📢 Новый заказ на сайт!\n\n"
        f"♦️ Название:\n — {user_data['name']}\n"
        f"♦️ Желаемый домен:\n — {user_data['domain']}\n"
        f"♦️ Страницы сайта:\n — {user_data['layout']}\n"
        f"♦️ Функционал сайта:\n — {user_data['func']}\n"
        f"♦️ Вспомогательные системы:\n — {user_data['addons']}\n"
        f"♦️ Примеры:\n — {user_data['examples']}\n"
        f"♦️ Дизайн:\n — {user_data['design']}\n"
        f"♦️ Дополнительная информация:\n — {user_data['extra']}\n"
        f"♦️ Сроки:\n — {user_data['dead']}\n"
        f"♦️ Откуда узнали о нас:\n — {user_data['source']}\n\n"
        f"Заказчик: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
    )

    await safe_send_message(GROUP_ID, full_text)
    await message.answer("✅ Ваш заказ на сайт принят!", reply_markup=main_menu)
    await state.clear()


async def safe_send_message(chat_id: int, text: str):
    max_length = 4096
    for i in range(0, len(text), max_length):
        await bot.send_message(chat_id, text[i:i + max_length])


@router.message(Command("cancel"))
async def cancel_order_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🚫 Заказ отменён. Вы вернулись в главное меню.", reply_markup=main_menu)


@router.message(OrderState.waiting_for_nameSite)
async def process_name_site(message: types.Message, state: FSMContext):
    await process_order_site_step(message, state, 'name')


@router.message(OrderState.waiting_for_siteDomain)
async def process_domain(message: types.Message, state: FSMContext):
    await process_order_site_step(message, state, 'domain')


@router.message(OrderState.waiting_for_layoutSite)
async def process_layout(message: types.Message, state: FSMContext):
    await process_order_site_step(message, state, 'layout')


@router.message(OrderState.waiting_for_funcSite)
async def process_func(message: types.Message, state: FSMContext):
    await process_order_site_step(message, state, 'func')


@router.message(OrderState.waiting_for_addonsSite)
async def process_addons(message: types.Message, state: FSMContext):
    await process_order_site_step(message, state, 'addons')


@router.message(OrderState.waiting_for_examplesSite)
async def process_examples(message: types.Message, state: FSMContext):
    await process_order_site_step(message, state, 'examples')


@router.message(OrderState.waiting_for_designSite)
async def process_design(message: types.Message, state: FSMContext):
    await process_order_site_step(message, state, 'design')


@router.message(OrderState.waiting_for_extraInfoSite)
async def process_extra(message: types.Message, state: FSMContext):
    await process_order_site_step(message, state, 'extra')


@router.message(OrderState.waiting_for_deadlineSite)
async def process_dead(message: types.Message, state: FSMContext):
    await process_order_site_step(message, state, 'dead')


@router.message(OrderState.waiting_for_sourceSite)
async def process_source_site(message: types.Message, state: FSMContext):
    await process_order_site_step(message, state, 'source')

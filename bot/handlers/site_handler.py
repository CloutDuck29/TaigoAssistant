from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.keyboards import minecraft_menu, yes_no_menu, main_menu, how_do_you_know_us, deadline
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID

router = Router()

@router.message(OrderState.waiting_for_nameSite)
async def process_name_site(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажите свой домен (при наличии)")
    await state.set_state(OrderState.waiting_for_siteDomain)

@router.message(OrderState.waiting_for_siteDomain)
async def process_domain(message: types.Message, state: FSMContext):
    await state.update_data(domain=message.text)
    await message.answer("Укажите какие страницы должны быть на сайте и их описание")
    await state.set_state(OrderState.waiting_for_layoutSite)

@router.message(OrderState.waiting_for_layoutSite)
async def process_layout(message: types.Message, state: FSMContext):
    await state.update_data(layout=message.text)
    await message.answer("Укажите функционал сайта и какие задачи он должен решать")
    await state.set_state(OrderState.waiting_for_funcSite)

@router.message(OrderState.waiting_for_funcSite)
async def process_func(message: types.Message, state: FSMContext):
    await state.update_data(func=message.text)
    await message.answer("Укажите, есть ли вспомогательные системы, с которыми должен работать сайт")
    await state.set_state(OrderState.waiting_for_addonsSite)

@router.message(OrderState.waiting_for_addonsSite)
async def process_addons(message: types.Message, state: FSMContext):
    await state.update_data(addons=message.text)
    await message.answer("Предоставьте примеры сайтов наподобие, на которые мы могли бы ориентироваться (при наличии)")
    await state.set_state(OrderState.waiting_for_examplesSite)


@router.message(OrderState.waiting_for_examplesSite)
async def process_examples(message: types.Message, state: FSMContext):
    await state.update_data(examples=message.text)
    await message.answer("Предоставьте ссылку на дизайн (при наличии)")
    await state.set_state(OrderState.waiting_for_designSite)

@router.message(OrderState.waiting_for_designSite)
async def process_design(message: types.Message, state: FSMContext):
    await state.update_data(design=message.text)
    await message.answer("Здесь Вы можете описать что-то дополнительное, что было упущено в нашей форме на Ваш взгляд, необходимое Вашему проекту")
    await state.set_state(OrderState.waiting_for_extraInfoSite)

@router.message(OrderState.waiting_for_extraInfoSite)
async def process_extra(message: types.Message, state: FSMContext):
    await state.update_data(extra=message.text)
    await message.answer("Есть ли у Вас пожелания по поводу сроков?", reply_markup=deadline)
    await state.set_state(OrderState.waiting_for_deadlineSite)


@router.message(OrderState.waiting_for_deadlineSite)
async def process_dead(message: types.Message, state: FSMContext):
    await state.update_data(dead=message.text)
    await message.answer("Откуда Вы узнали о нашей студии?", reply_markup=how_do_you_know_us)
    await state.set_state(OrderState.waiting_for_sourceSite)


@router.message(OrderState.waiting_for_sourceSite)
async def process_source_site(message: types.Message, state: FSMContext):
    await state.update_data(source=message.text)

    user_data = await state.get_data()

    # Сформируем полный текст для отправки
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
        f"♦️ Откуда узнали о нас:\n — {user_data['source']}\n"
        f"Заказчик: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
    )

    # Используем безопасную отправку сообщения
    await safe_send_message(GROUP_ID, full_text)

    await message.answer("✅ Ваш заказ на сайт принят!", reply_markup=main_menu)

    await state.clear()


async def safe_send_message(chat_id: int, text: str):
    max_length = 4096
    for i in range(0, len(text), max_length):
        await bot.send_message(chat_id, text[i:i + max_length])
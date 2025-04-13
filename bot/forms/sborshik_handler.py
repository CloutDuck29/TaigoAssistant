from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bot.keyboards import main_menu
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID

router = Router()

questions = [
    ("fio", "📋 Введите свое ФИО", OrderState.waiting_for_fio),
    ("name", "Ваша дата рождения (дд.мм.гггг)?", OrderState.waiting_for_birthdate),
    ("birthdate", "Ваш опыт в годах", OrderState.waiting_for_experience),
    ("experience", "1️⃣ Какой у Вас опыт в настройке и управлении серверами Minecraft?\nКакие типы серверов (например, Bukkit, Spigot, Paper) Вы настраивали?", OrderState.waiting_for_experienceInServers),
    ("experienceInServer", "2️⃣ Как Вы подходите к выбору и установке плагинов?", OrderState.waiting_for_choosePlugin),
    ("choosePlugins", "3️⃣ Как Вы решаете проблемы совместимости между плагинами?", OrderState.waiting_for_problemsInPlugins),
    ("problemsInPlugins", "4️⃣ Какие меры Вы предпринимаете для оптимизации работы сервера?", OrderState.waiting_for_optimizationPluginsOnServer),
    ("optimizationPlugin", "5️⃣ Как Вы решаете задачи по миграции серверов или обновлению плагинов?", OrderState.waiting_for_tasksOnMigrationsAndUpd),
    ("updatePlugin", "6️⃣ Какие инструменты Вы используете для диагностики проблем с плагинами?", OrderState.waiting_for_monitoringProblems),
    ("monitoringProblems", "7️⃣ Как Вы поддерживаете актуальность плагинов?", OrderState.waiting_for_actualizationOfPlugin),
    ("actualizationPlugin", "8️⃣ Прикрепите портфолио (ссылки GitHub, Behance и т.д.)", OrderState.waiting_for_portfolioPlugin),
    ("portfolioPlugin", None, None)
]

field_to_state = {field: state for field, _, state in questions if state is not None}
state_to_field = {state: field for field, _, state in questions if state is not None}

@router.message(Command("cancel"))
async def cancel_order_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🚫 Создание заказа отменено. Вы вернулись в главное меню.", reply_markup=main_menu)

@router.message()
async def handle_plugin_question(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    field = state_to_field.get(current_state)

    if not field:
        return

    await state.update_data({field: message.text})

    current_index = next((i for i, (f, _, _) in enumerate(questions) if f == field), None)
    if current_index is not None and current_index + 1 < len(questions):
        next_field, question, next_state = questions[current_index + 1]
        if question:
            await message.answer(question, reply_markup=ReplyKeyboardRemove())
        if next_state:
            await state.set_state(next_state)
        else:
            await complete_form(message, state)

async def complete_form(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    text = (
        f"📢 Новый кандидат в команду сборщиков!\n\n"
        f"🔹 ФИО:\n — {user_data.get('fio')}\n"
        f"🔹 Дата рождения:\n — {user_data.get('name')}\n"
        f"🔹 Опыт в годах:\n — {user_data.get('birthdate')}\n"
        f"🔹 Коротко о опыте в серверах:\n — {user_data.get('experience')}\n"
        f"🔹 Настройка плагинов:\n — {user_data.get('experienceInServer')}\n"
        f"🔹 Совместимость плагинов:\n — {user_data.get('choosePlugins')}\n"
        f"🔹 Оптимизация:\n — {user_data.get('problemsInPlugins')}\n"
        f"🔹 Обновления:\n — {user_data.get('optimizationPlugin')}\n"
        f"🔹 Диагностика:\n — {user_data.get('updatePlugin')}\n"
        f"🔹 Актуальность:\n — {user_data.get('monitoringProblems')}\n"
        f"🔹 Портфолио:\n — {user_data.get('actualizationPlugin')}\n\n"
        f"Кандидат: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
    )

    await bot.send_message(GROUP_ID, text)
    await message.answer("✅ Ваша заявка отправлена. Ожидайте обратной связи!", reply_markup=main_menu)
    await state.clear()

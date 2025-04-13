from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bot.keyboards import main_menu
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID

router = Router()

plugin_specialist_questions = {
    'name': {"question": "Ваша дата рождения (дд.мм.гггг)?", "next_state": OrderState.waiting_for_birthdate},
    'birthdate': {"question": "Ваш опыт в годах", "next_state": OrderState.waiting_for_experience},
    'experience': {"question": "1️⃣ Какой у Вас опыт в настройке и управлении серверами Minecraft?\nКакие типы серверов (например, Bukkit, Spigot, Paper) Вы настраивали?", "next_state": OrderState.waiting_for_experienceInServers},
    'experienceInServer': {"question": "2️⃣ Как Вы подходите к выбору и установке плагинов для серверов Minecraft?\nС какими плагинами Вы работали, и как обеспечивали их совместимость?", "next_state": OrderState.waiting_for_choosePlugin},
    'choosePlugins': {"question": "3️⃣ Как Вы решаете проблемы совместимости между плагинами?\nКакие шаги предпринимаете, чтобы плагины не конфликтовали друг с другом?", "next_state": OrderState.waiting_for_problemsInPlugins},
    'problemsInPlugins': {"question": "4️⃣ Какие меры Вы предпринимаете для оптимизации работы сервера и плагинов?\nКак проверяете, чтобы сервер не испытывал лагов и работал стабильно при большой нагрузке?", "next_state": OrderState.waiting_for_optimizationPluginsOnServer},
    'optimizationPlugin': {"question": "5️⃣ Как Вы решаете задачи по миграции серверов или обновлению плагинов?\nКакие шаги предпринимаете для минимизации рисков при обновлениях?", "next_state": OrderState.waiting_for_tasksOnMigrationsAndUpd},
    'updatePlugin': {"question": "6️⃣ Какие инструменты или подходы Вы используете для мониторинга состояния сервера и диагностики проблем с плагинами?", "next_state": OrderState.waiting_for_monitoringProblems},
    'monitoringProblems': {"question": "7️⃣ Как Вы поддерживаете актуальность плагинов и сервера в целом?\nКак часто Вы обновляете плагины и проверяете их на совместимость с новыми версиями Minecraft?", "next_state": OrderState.waiting_for_actualizationOfPlugin},
    'actualizationPlugin': {"question": "8️⃣ Прикрепите портфолио Ваших работ (ссылка Github, behance, imgur и др)", "next_state": OrderState.waiting_for_portfolioPlugin},
    'portfolioPlugin': {"question": None, "next_state": None}
}

@router.message(Command("cancel"))
async def cancel_order_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🚫 Заказ отменён. Вы вернулись в главное меню.", reply_markup=main_menu)

async def process_plugin_specialist_step(message: types.Message, state: FSMContext, field: str):
    await state.update_data({field: message.text})
    step_info = plugin_specialist_questions[field]

    if step_info["next_state"]:
        await message.answer(step_info["question"], reply_markup=ReplyKeyboardRemove())
        await state.set_state(step_info["next_state"])
    else:
        await complete_sborshik_form(message, state)

@router.message(OrderState.waiting_for_fio)
async def process_name(message: types.Message, state: FSMContext):
    await process_plugin_specialist_step(message, state, 'name')

@router.message(OrderState.waiting_for_birthdate)
async def process_birth(message: types.Message, state: FSMContext):
    await process_plugin_specialist_step(message, state, 'birthdate')

@router.message(OrderState.waiting_for_experience)
async def process_year(message: types.Message, state: FSMContext):
    await process_plugin_specialist_step(message, state, 'experience')

@router.message(OrderState.waiting_for_experienceInServers)
async def process_q1(message: types.Message, state: FSMContext):
    await process_plugin_specialist_step(message, state, 'experienceInServer')

@router.message(OrderState.waiting_for_choosePlugin)
async def process_q2(message: types.Message, state: FSMContext):
    await process_plugin_specialist_step(message, state, 'choosePlugins')

@router.message(OrderState.waiting_for_problemsInPlugins)
async def process_q3(message: types.Message, state: FSMContext):
    await process_plugin_specialist_step(message, state, 'problemsInPlugins')

@router.message(OrderState.waiting_for_optimizationPluginsOnServer)
async def process_q4(message: types.Message, state: FSMContext):
    await process_plugin_specialist_step(message, state, 'optimizationPlugin')

@router.message(OrderState.waiting_for_tasksOnMigrationsAndUpd)
async def process_q5(message: types.Message, state: FSMContext):
    await process_plugin_specialist_step(message, state, 'updatePlugin')

@router.message(OrderState.waiting_for_monitoringProblems)
async def process_q6(message: types.Message, state: FSMContext):
    await process_plugin_specialist_step(message, state, 'monitoringProblems')

@router.message(OrderState.waiting_for_actualizationOfPlugin)
async def process_q7(message: types.Message, state: FSMContext):
    await process_plugin_specialist_step(message, state, 'actualizationPlugin')

@router.message(OrderState.waiting_for_portfolioPlugin)
async def process_q8(message: types.Message, state: FSMContext):
    await process_plugin_specialist_step(message, state, 'portfolioPlugin')

async def complete_sborshik_form(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.send_message(
        GROUP_ID,
        f"📢 Новый кандидат в команду сборщиков!\n\n"
        f"🔹 ФИО:\n — {user_data['name']}\n"
        f"🔹 Дата рождения:\n — {user_data['birthdate']}\n"
        f"🔹 Опыт в годах:\n — {user_data['experience']}\n"
        f"🔹 Коротко о опыте в серверах:\n — {user_data['experienceInServer']}\n"
        f"🔹 Настройка плагинов и подбор:\n — {user_data['choosePlugins']}\n"
        f"🔹 Совместимость плагинов и их конфликты:\n — {user_data['problemsInPlugins']}\n"
        f"🔹 Лаги и оптимизация:\n — {user_data['optimizationPlugin']}\n"
        f"🔹 Обновление плагинов:\n — {user_data['updatePlugin']}\n"
        f"🔹 Диагностика проблем:\n — {user_data['monitoringProblems']}\n"
        f"🔹 Актуальность плагинов:\n — {user_data['actualizationPlugin']}\n"
        f"🔹 Примеры работ:\n — {user_data['portfolioPlugin']}\n\n"
        f"Кандидат: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
    )
    await message.answer("✅ Ваша заявка на вступление в команду на должность Сборщик MineCraft принята. Ожидайте обратной связи!", reply_markup=main_menu)
    await state.clear()

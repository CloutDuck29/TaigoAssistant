from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.keyboards import minecraft_menu, yes_no_menu, main_menu, how_do_you_know_us, deadline
from bot.states import OrderState
from bot.loader import bot
from bot.config import GROUP_ID
from aiogram.filters import Command

router = Router()

order_build_steps = {
    'name': {"question": "Ваша дата рождения (дд.мм.гггг)?", "next_state": OrderState.waiting_for_birthdatePlugin},
    'birthdate': {"question": "Ваш опыт в годах", "next_state": OrderState.waiting_for_experienceInYearsInPlugins},
    'experience': {"question": "1️⃣ Какой у Вас опыт в разработке плагинов для Minecraft? C какими платформами (Bukkit, Spigot, Paper) Вы работали?", "next_state": OrderState.waiting_for_experiencePlugin},
    'plugin_experience': {"question": "2️⃣ Какой Ваш уровень владения языком Java/Kotlin? Работали ли Вы с другими языками или технологиями, связанными с разработкой плагинов?", "next_state": OrderState.waiting_for_languagePlugin},
    'language_experience': {"question": "3️⃣ Можете ли Вы привести пример плагина, который Вы разработали? Какие основные функции он выполняет, и какие задачи решает?", "next_state": OrderState.waiting_for_exampleOfPlugin},
    'plugin_example': {"question": "4️⃣ Как Вы подходите к оптимизации плагинов для серверов Minecraft? Какие шаги предпринимаете, чтобы избежать лагов и улучшить производительность?", "next_state": OrderState.waiting_for_optimizationOfPlugin},
    'optimization_plugin': {"question": "5️⃣ Есть ли у Вас опыт работы с базами данных в плагинах (например, MySQL или SQLite)?", "next_state": OrderState.waiting_for_databaseOfPlugin},
    'database_experience': {"question": "6️⃣ Какие методы тестирования Вы используете при разработке плагинов? Как Вы справляетесь с отладкой ошибок и багов?", "next_state": OrderState.waiting_for_testsOfPlugin},
    'tests_plugin': {"question": "7️⃣ Как Вы решаете вопросы совместимости плагинов с другими плагинами на сервере?", "next_state": OrderState.waiting_for_compsOfPlugin},
    'comp_plugin': {"question": "8️⃣ Как Вы обычно проектируете конфигурационные файлы для плагинов (например, YAML или JSON)? Как Вы обеспечиваете их гибкость и удобство для администраторов серверов?", "next_state": OrderState.waiting_for_configOfPlugin},
    'config_plugin': {"question": "9️⃣ Как Вы реализуете взаимодействие плагинов с игроками, например, через команды, GUI или уведомления?", "next_state": OrderState.waiting_for_guiOfPlugin},
    'gui_plugin': {"question": "9️⃣ Прикрепите портфолио Ваших работ (ссылка Github, behance, imgur и др)","next_state": OrderState.waiting_for_portfolioPluginNew},
    'portfolio': {"question": None, "next_state": None}
}


async def process_order_build_step(message: types.Message, state: FSMContext, field: str):
    if message.text.lower() == "/cancel":
        await state.clear()
        await message.answer("🚫 Заполнение анкеты отменено. Вы вернулись в главное меню.", reply_markup=main_menu)
        return

    await state.update_data({field: message.text})

    step_info = order_build_steps[field]
    if step_info["question"]:
        text = step_info["question"]

        if field == "name":
            text += "\n\n❗ Если хотите отменить заказ — введите /cancel"

        await message.answer(text, reply_markup=step_info.get("keyboard", ReplyKeyboardRemove()))

    if step_info["next_state"]:
        await state.set_state(step_info["next_state"])
    else:
        await complete_plugin_form(message, state)

async def complete_plugin_form(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.send_message(
        GROUP_ID,
        f"📢 Новый кандидат на разработчика плагинов!\n\n"
        f"🔹 ФИО:\n — {user_data['name']}\n"
        f"🔹 Дата рождения:\n — {user_data['birthdate']}\n"
        f"🔹 Опыт в годах:\n — {user_data['experience']}\n"
        f"🔹 Опыт работы с плагинами:\n — {user_data['plugin_experience']}\n"
        f"🔹 Опыт в языках:\n — {user_data['language_experience']}\n"
        f"🔹 Пример плагина:\n — {user_data['plugin_example']}\n"
        f"🔹 Оптимизация плагина:\n — {user_data['optimization_plugin']}\n"
        f"🔹 Опыт в БД:\n — {user_data['database_experience']}\n"
        f"🔹 Тестирование плагина:\n — {user_data['tests_plugin']}\n"
        f"🔹 Совместимость:\n — {user_data['comp_plugin']}\n"
        f"🔹 Работа с конфигами:\n — {user_data['config_plugin']}\n"
        f"🔹 Работа с GUI:\n — {user_data['gui_plugin']}\n"       
        f"🔹 Портфолио:\n — {user_data['portfolio']}\n\n"       
        f"Отправитель: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
    )
    await message.answer("✅ Ваша заявка на вступление в рассмотрении. Ожидайте обратной связи!", reply_markup=main_menu)
    await state.clear()

@router.message(OrderState.waiting_for_fioPlugin)
async def process_fio(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'name')

@router.message(OrderState.waiting_for_birthdatePlugin)
async def process_birthdate(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'birthdate')

@router.message(OrderState.waiting_for_experienceInYearsInPlugins)
async def process_experience_inyears(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'experience')

@router.message(OrderState.waiting_for_experiencePlugin)
async def process_plugin_experiencefact(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'plugin_experience')

@router.message(OrderState.waiting_for_languagePlugin)
async def process_language_exp(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'language_experience')

@router.message(OrderState.waiting_for_exampleOfPlugin)
async def process_examp_plug(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'plugin_example')

@router.message(OrderState.waiting_for_optimizationOfPlugin)
async def process_optimization_plug(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'optimization_plugin')

@router.message(OrderState.waiting_for_databaseOfPlugin)
async def process_data_plug(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'database_experience')

@router.message(OrderState.waiting_for_testsOfPlugin)
async def process_test_plug(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'tests_plugin')

@router.message(OrderState.waiting_for_compsOfPlugin)
async def process_comp_plug(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'comp_plugin')

@router.message(OrderState.waiting_for_configOfPlugin)
async def process_config_plugin(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'config_plugin')

@router.message(OrderState.waiting_for_guiOfPlugin)
async def process_gui_plugin(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'gui_plugin')

@router.message(OrderState.waiting_for_portfolioPluginNew)
async def process_gui_plugin(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'portfolio')

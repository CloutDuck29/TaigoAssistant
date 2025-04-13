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
    'name': {"question": "Ваша дата рождения (дд.мм.гггг)?", "next_state": OrderState.waiting_for_birthdate},
    'birthdate': {"question": "Ваш опыт в годах", "next_state": OrderState.waiting_for_experience},
    'experience': {"question": "1️⃣ Какой у Вас опыт в настройке и управлении серверами Minecraft?\nКакие типы серверов (например, Bukkit, Spigot, Paper) Вы настраивали?", "next_state": OrderState.waiting_for_experienceInServers},
    'experienceInServer': {"question": "2️⃣ Как Вы подходите к выбору и установке плагинов?", "next_state": OrderState.waiting_for_choosePlugin},
    'choosePlugins': {"question": "3️⃣ Как Вы решаете проблемы совместимости между плагинами?", "next_state": OrderState.waiting_for_problemsInPlugins},
    'problemsInPlugins': {"question": "4️⃣ Какие меры Вы предпринимаете для оптимизации работы сервера?", "next_state": OrderState.waiting_for_optimizationPluginsOnServer},
    'optimizationPlugin': {"question": "5️⃣ Как Вы решаете задачи по миграции серверов или обновлению плагинов?", "next_state": OrderState.waiting_for_tasksOnMigrationsAndUpd},
    'updatePlugin': {"question": "6️⃣ Какие инструменты Вы используете для диагностики проблем с плагинами?", "next_state": OrderState.waiting_for_monitoringProblems},
    'monitoringProblems': {"question": "7️⃣ Как Вы поддерживаете актуальность плагинов?", "next_state": OrderState.waiting_for_actualizationOfPlugin},
    'actualizationPlugin': {"question": "8️⃣ Прикрепите портфолио (ссылки GitHub, Behance и т.д.)", "next_state": OrderState.waiting_for_portfolioPlugin},
    'portfolioPlugin': {"question": None, "next_state": None}
}

async def process_order_build_step(message: types.Message, state: FSMContext, field: str):
    if message.text.lower() == "/cancel":
        await state.clear()
        await message.answer("🚫 Заказ отменён. Вы вернулись в главное меню.", reply_markup=main_menu)
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
        await complete_build_order(message, state)

async def complete_build_order(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.send_message(
        GROUP_ID,
        f"📢 Новый кандидат на сборщика!\n\n"
        f"🔹 ФИО:\n — {user_data['name']}\n"
        f"🔹 Дата рождения:\n — {user_data['birthdate']}\n"
        f"🔹 Опыт в годах:\n — {user_data['experience']}\n"
        f"🔹 Опыт в настройке и управлении серверами Minecraft:\n — {user_data['experienceInServer']}\n"
        f"🔹 Подход к выбору и установке плагинов:\n — {user_data['choosePlugins']}\n"
        f"🔹 Решение проблем совместимости между плагинами:\n — {user_data['problemsInPlugins']}\n"
        f"🔹 Меры по оптимизации работы сервера:\n — {user_data['optimizationPlugin']}\n"
        f"🔹 Задачи по миграции серверов или обновлению плагинов:\n — {user_data['updatePlugin']}\n"
        f"🔹 Инструменты для диагностики проблем с плагинами:\n — {user_data['monitoringProblems']}\n"
        f"🔹 Поддержка актуальности плагинов:\n — {user_data['actualizationPlugin']}\n"
        f"🔹 Портфолио (ссылки GitHub, Behance и т.д.):\n — {user_data['portfolioPlugin']}\n\n"
        f"Заказчик: {message.from_user.full_name} (@{message.from_user.username or 'Без юзернейма'})"
    )
    await message.answer("✅ Ваша заявка на вступление в рассмотрении. Ожидайте обратной связи!", reply_markup=main_menu)
    await state.clear()

@router.message(Command("cancel"))
async def cancel_order_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🚫 Заказ отменён. Вы вернулись в главное меню.", reply_markup=main_menu)

@router.message(OrderState.waiting_for_fio)
async def process_fio(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'name')


@router.message(OrderState.waiting_for_birthdate)
async def process_birthdate(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'birthdate')


@router.message(OrderState.waiting_for_experience)
async def process_experience(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'experience')


@router.message(OrderState.waiting_for_experienceInServers)
async def process_experienceInServers(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'experienceInServer')


@router.message(OrderState.waiting_for_choosePlugin)
async def process_choosePlugin(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'choosePlugins')


@router.message(OrderState.waiting_for_problemsInPlugins)
async def process_problemsInPlugins(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'problemsInPlugins')


@router.message(OrderState.waiting_for_optimizationPluginsOnServer)
async def process_optimizationPluginsOnServer(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'optimizationPlugin')


@router.message(OrderState.waiting_for_tasksOnMigrationsAndUpd)
async def process_tasksOnMigrationsAndUpd(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'updatePlugin')


@router.message(OrderState.waiting_for_monitoringProblems)
async def process_monitoringProblems(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'monitoringProblems')


@router.message(OrderState.waiting_for_actualizationOfPlugin)
async def process_actualizationOfPlugin(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'actualizationPlugin')


@router.message(OrderState.waiting_for_portfolioPlugin)
async def process_portfolioPlugin(message: types.Message, state: FSMContext):
    await process_order_build_step(message, state, 'portfolioPlugin')


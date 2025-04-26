from aiogram import types, Router
from aiogram.filters import Command
from bot.keyboards import main_menu, info_menu

router = Router()

buttons_info = {
    "ℹ️ Информация": {
        "text": "📌 TaigoStudio – команда профессионалов, создающих Minecraft-серверы, моды, лаунчеры и сайты.\n\n"
                "🔹 Мы работаем с 2021 года и сотрудничаем с клиентами по всему миру! 🌍",
        "reply_markup": info_menu
    },
    "🎨 Портфолио": {
        "text": "🎨 <b>Наши работы</b>: https://vk.com/taigostudio",
        "parse_mode": "HTML"
    },
    "❓FAQ": {
        "text": "❓ <b>Частые вопросы:</b>\n\n"
                "🔹 Сколько стоит разработка? – от 2500₽, зависит от сложности.\n"
                "🔹 Как долго делается проект? – от 3 дней.\n"
                "🔹 Как оплатить? – по договорённости (ИП, Криптовалюта, Фриланс).",
        "parse_mode": "HTML"
    },
    "📞 Контакты": {
        "text": "📞 <b>Контакты для связи:</b>\n\n"
                "🔹 Telegram: @taigo_official\n"
                "🔹 ВКонтакте: https://vk.com/taigostudio",
        "parse_mode": "HTML"
    },
    "⭐️ Отзывы": {
        "text": "⭐️ <b>Отзывы наших клиентов:</b>\n\n"
                "📖 https://vk.com/topic-166798462_47602007",
        "parse_mode": "HTML"
    },
    "🌍 Сайт": {
        "text": "🌍 <b>Наш сайт:</b> https://taigo.xyz",
        "parse_mode": "HTML"
    }
}

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот студии TaigoStudio.\n\n"
        "Мы создаем Minecraft-проекты и разрабатываем ПО.\n\n"
        "📆 Работаем с 2021 года!",
        reply_markup=main_menu
    )

@router.message(lambda message: message.text in buttons_info)
async def handle_button(message: types.Message):
    button_data = buttons_info[message.text]
    await message.answer(
        button_data["text"],
        parse_mode=button_data.get("parse_mode", None),
        reply_markup=button_data.get("reply_markup", None)
    )

@router.message(lambda message: message.text == "🏚 В главное меню")
async def back_to_main(message: types.Message):
    # если FSM не используется, просто отправляем меню
    await message.answer(
        "Вы вернулись в главное меню. Чем могу помочь?",
        reply_markup=main_menu
    )
from aiogram import types, Router
from aiogram.filters import Command
from bot.keyboards import main_menu, info_menu

router = Router()

# Команда /start
@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот студии TaigoStudio.\n\n"
        "Мы создаем Minecraft-проекты и разрабатываем ПО.\n\n"
        "📆 Работаем с 2021 года!",
        reply_markup=main_menu
    )

# Обработка кнопок
@router.message(lambda message: message.text == "ℹ️ Информация")
async def info_button(message: types.Message):
    await message.answer(
        "📌 TaigoStudio – команда профессионалов, создающих Minecraft-серверы, моды, лаунчеры и сайты.\n\n"
        "🔹 Мы работаем с 2021 года и сотрудничаем с клиентами по всему миру! 🌍",
        reply_markup=info_menu
    )

@router.message(lambda message: message.text == "🎨 Портфолио")
async def portfolio_button(message: types.Message):
    await message.answer(
        "🎨 <b>Наши работы</b>: https://vk.com/taigostudio",
        parse_mode="HTML"
    )

@router.message(lambda message: message.text == "❓FAQ")
async def faq_button(message: types.Message):
    await message.answer(
        "❓ <b>Частые вопросы:</b>\n\n"
        "🔹 Сколько стоит разработка? – от 2500₽, зависит от сложности.\n"
        "🔹 Как долго делается проект? – от 3 дней.\n"
        "🔹 Как оплатить? – по договорённости (ИП, Криптовалюта, Фриланс).",
        parse_mode="HTML"
    )

@router.message(lambda message: message.text == "📞 Контакты")
async def contacts_button(message: types.Message):
    await message.answer(
        "📞 <b>Контакты для связи:</b>\n\n"
        "🔹 Telegram: @taigo_official\n"
        "🔹 ВКонтакте: https://vk.com/taigostudio",
        parse_mode="HTML"
    )

@router.message(lambda message: message.text == "⭐️ Отзывы")
async def reviews_button(message: types.Message):
    await message.answer(
        "⭐️ <b>Отзывы наших клиентов:</b>\n\n"
        "📖 https://vk.com/topic-166798462_47602007",
        parse_mode="HTML"
    )

@router.message(lambda message: message.text == "👩🏻‍💻 Поддержка")
async def support_button(message: types.Message):
    await message.answer(
        "🆘 Нужна помощь? Напишите нам в поддержку: @taigo_official"
    )

@router.message(lambda message: message.text == "🌍 Сайт")
async def site_button(message: types.Message):
    await message.answer(
        "🌍 <b>Наш сайт:</b> https://taigo.xyz",
        parse_mode="HTML"
    )

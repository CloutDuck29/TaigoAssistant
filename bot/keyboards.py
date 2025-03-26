from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="ℹ️ Информация"), KeyboardButton(text="📝 Заказать")],
        [KeyboardButton(text="🎨 Портфолио"), KeyboardButton(text="❓FAQ")],
        [KeyboardButton(text="📞 Контакты"), KeyboardButton(text="⭐️ Отзывы")],
        [KeyboardButton(text="👩🏻‍💻 Поддержка"), KeyboardButton(text="🌍 Сайт")]
    ],
    resize_keyboard=True
)

project_type_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🟢 Minecraft")],
        [KeyboardButton(text="🔵 ПО")]
    ],
    resize_keyboard=True
)

minecraft_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Лаунчер"), KeyboardButton(text="Сборка")],
        [KeyboardButton(text="Постройка"), KeyboardButton(text="Плагин")]
    ],
    resize_keyboard=True
)

software_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сайт"), KeyboardButton(text="Игра")],
        [KeyboardButton(text="Приложение")]
    ],
    resize_keyboard=True
)

yes_no_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
    ],
    resize_keyboard=True
)

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

how_do_you_know_us = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="ВК"), KeyboardButton(text="Kwork")],
        [KeyboardButton(text="Fiverr"), KeyboardButton(text="В интернете")],
        [KeyboardButton(text="Посоветовали")]
    ],
    resize_keyboard=True
)

deadline = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Нет"), KeyboardButton(text="Не больше недели")],
        [KeyboardButton(text="Не больше двух недель"), KeyboardButton(text="Не больше месяца")],
        [KeyboardButton(text="Не больше трех месяцев")]
    ],
    resize_keyboard=True
)

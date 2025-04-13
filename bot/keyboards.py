from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Функция для генерации клавиатуры
def generate_keyboard(buttons: list) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button) for button in row] for row in buttons],
        resize_keyboard=True
    )

# Меню
main_menu = generate_keyboard([["ℹ️ Информация", "📝 Заказать"]])

info_menu = generate_keyboard([
    ["🎨 Портфолио", "❓FAQ"],
    ["📞 Контакты", "⭐️ Отзывы"],
    ["👩🏻‍💻 Поддержка", "🌍 Сайт"],
    ["📝 Заказать"]
])

project_type_menu = generate_keyboard([["🟢 Minecraft"], ["🔵 ПО"]])

minecraft_menu = generate_keyboard([
    ["Лаунчер", "Сборка"],
    ["Постройка", "Плагин"]
])

software_menu = generate_keyboard([
    ["Сайт", "Игра"],
    ["Приложение"]
])

yes_no_menu = generate_keyboard([["Да", "Нет"]])

how_do_you_know_us = generate_keyboard([
    ["ВК", "Kwork"],
    ["Fiverr", "В интернете"],
    ["Посоветовали"]
])

deadline = generate_keyboard([
    ["Нет", "Не больше недели"],
    ["Не больше двух недель", "Не больше месяца"],
    ["Не больше трех месяцев"]
])

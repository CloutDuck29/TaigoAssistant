from aiogram.fsm.state import State, StatesGroup

class OrderState(StatesGroup):
    waiting_for_project_type = State()  # добавьте это состояние
    waiting_for_category = State()
    waiting_for_name = State()
    waiting_for_version = State()
    waiting_for_socials = State()
    waiting_for_colors = State()
    waiting_for_mode = State()
    waiting_for_functionality = State()
    waiting_for_spawn = State()
    waiting_for_holograms = State()
    waiting_for_plugins = State()
    waiting_for_launcher = State()
    waiting_for_icon = State()
    waiting_for_donations = State()
    waiting_for_additional = State()
    waiting_for_deadline = State()
    waiting_for_support = State()
    waiting_for_source = State()

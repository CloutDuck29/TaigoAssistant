from aiogram.fsm.state import State, StatesGroup

class OrderState(StatesGroup):
    waiting_for_project_type = State()
    waiting_for_category = State()
    waiting_for_name = State()
    waiting_for_version = State()
    waiting_for_socials = State()
    waiting_for_spawn = State()
    waiting_for_deadline = State()

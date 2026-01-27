from aiogram.fsm.state import State, StatesGroup


class WaitingPhone(StatesGroup):
    waiting_for_phone: State = State()


class Registration(WaitingPhone):
    pass


class ResetPassword(WaitingPhone):
    pass

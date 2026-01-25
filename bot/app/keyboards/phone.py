from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb_phone = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📞 Отправить номер", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

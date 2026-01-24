from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

router = Router()

kb_phone = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📞 Отправить номер", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user = message.from_user
    if user is None:
        raise ValueError()
    await message.answer(
        f"Привет, {user.full_name}! Поделись своим номером телефона:",
        reply_markup=kb_phone,
    )


@router.message(F.text == "/phone")
async def ask_phone(message: Message):
    await message.answer("Нажми кнопку, чтобы отправить номер телефона:", reply_markup=kb_phone)


@router.message(F.contact)
async def got_phone(message: Message):
    contact = message.contact
    user = message.from_user

    if not contact or not user:
        return
    if contact.user_id != user.id:
        await message.answer("Пожалуйста, отправь *свой* номер через кнопку.")
        return

    await message.answer(f"Спасибо! Твой номер: {contact.phone_number}")

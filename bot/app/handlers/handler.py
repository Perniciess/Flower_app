from aiogram import F, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.phone import kb_phone
from app.states.registration import Registration

router = Router()


@router.message(CommandStart(deep_link=True))
async def command_start_handler(message: Message, command: CommandObject, state: FSMContext) -> None:
    user = message.from_user
    if user is None:
        raise ValueError()

    token = command.args
    await state.update_data(verification_token=token)

    await state.set_state(Registration.waiting_for_phone)

    await message.answer(
        f"Привет, {user.full_name}! Для регистрации нажми кнопку ниже:",
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

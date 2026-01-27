from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.core.config import settings
from app.keyboards.phone import kb_phone
from app.states.registration import ResetPassword

from .common import FlowConfig, handle_contact

router = Router()

FLOW = FlowConfig(
    redis_prefix="r",
    state_key="reset_token",
    target_state=ResetPassword.waiting_for_phone,
    complete_url=settings.COMPLETE_RESET,
    prompt_message="Подтвердите номер телефона для сброса пароля",
    success_message="Вы успешно подтвердили номер телефона! Продолжите сброс пароля на сайте",
)


@router.message(ResetPassword.waiting_for_phone, F.contact)
async def got_phone_reset(message: Message, state: FSMContext) -> None:
    await handle_contact(message, state, FLOW)


@router.message(ResetPassword.waiting_for_phone)
async def unknown_message_reset(message: Message) -> None:
    await message.answer("Нажмите кнопку ниже, чтобы отправить номер", reply_markup=kb_phone)

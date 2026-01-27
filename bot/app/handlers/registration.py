from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.core.config import settings
from app.keyboards.phone import kb_phone
from app.states.registration import Registration

from .common import FlowConfig, handle_contact

router = Router()

FLOW = FlowConfig(
    redis_prefix="v",
    state_key="verification_token",
    target_state=Registration.waiting_for_phone,
    complete_url=settings.REGISTER,
    prompt_message="Подтвердите номер телефона в течение 5 минут",
    success_message="Вы успешно подтвердили номер телефона!",
)


@router.message(Registration.waiting_for_phone, F.contact)
async def got_phone(message: Message, state: FSMContext) -> None:
    await handle_contact(message, state, FLOW)


@router.message(Registration.waiting_for_phone)
async def unknown_message(message: Message) -> None:
    await message.answer("Нажмите кнопку ниже, чтобы отправить номер", reply_markup=kb_phone)

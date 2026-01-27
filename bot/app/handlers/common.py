from dataclasses import dataclass

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message

from app.service.registration import complete, verify


@dataclass(frozen=True, slots=True)
class FlowConfig:
    redis_prefix: str
    state_key: str
    target_state: State
    complete_url: str
    prompt_message: str
    success_message: str


async def handle_contact(message: Message, state: FSMContext, flow: FlowConfig) -> None:
    contact = message.contact
    user = message.from_user

    if not contact or not user:
        await message.answer("Не удалось получить данные. Попробуйте ещё раз.")
        return

    if contact.user_id != user.id:
        await message.answer("Пожалуйста, отправь *свой* номер через кнопку.")
        return

    data = await state.get_data()
    token = data.get(flow.state_key)
    if not token:
        await message.answer("Сессия истекла. Начните заново на сайте.")
        await state.clear()
        return

    verified = await verify(token=token, type=flow.redis_prefix, phone_number=contact.phone_number)
    if not verified:
        await message.answer("Ваш номер телефона не соответствует")
        return

    result = await complete(token=token, url=flow.complete_url)
    if result:
        await message.answer(flow.success_message)
    else:
        await message.answer("Произошла ошибка. Попробуйте позже.")
    await state.clear()

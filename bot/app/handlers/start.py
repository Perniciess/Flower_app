from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.core.config import settings
from app.keyboards.phone import kb_phone
from app.service.registration import check_token

from .registration import FLOW as REGISTRATION_FLOW
from .reset_password import FLOW as RESET_FLOW

router = Router()


@router.message(CommandStart())
async def command_start_without_token(message: Message) -> None:
    await message.answer(f"Для регистрации перейдите на сайт: {settings.WEBSITE_URL}")


@router.message(CommandStart(deep_link=True))
async def command_start_handler(message: Message, command: CommandObject, state: FSMContext) -> None:
    if message.from_user is None:
        await message.answer("Ошибка: не удалось определить пользователя")
        return

    if not command.args:
        await message.answer("Откройте сайт, чтобы зарегистрироваться")
        return

    if command.args.startswith("reset_"):
        flow, token = RESET_FLOW, command.args.removeprefix("reset_")
    else:
        flow, token = REGISTRATION_FLOW, command.args

    if not await check_token(token=token, type=flow.redis_prefix):
        await message.answer("Код недействителен или истёк")
        return

    await state.update_data(data={flow.state_key: token})
    await state.set_state(flow.target_state)
    await message.answer(flow.prompt_message, reply_markup=kb_phone)

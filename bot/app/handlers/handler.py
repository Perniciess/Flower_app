from aiogram import F, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.phone import kb_phone
from app.service.registration import check_cache, complete_verify, verify_account
from app.states.registration import Registration

router = Router()


@router.message(CommandStart(deep_link=True))
async def command_start_handler(message: Message, command: CommandObject, state: FSMContext) -> None:
    user = message.from_user
    if user is None:
        raise ValueError()

    token = command.args
    if not token:
        await message.answer("Откройте сайт, чтобы зарегистрироваться")
        return

    cache = await check_cache(token=token)

    if not cache:
        await message.answer("Код недействителен или истёк")
        return

    await state.update_data(verification_token=token)

    await state.set_state(Registration.waiting_for_phone)

    await message.answer("Подтвердите номер телефона", reply_markup=kb_phone)


@router.message(Registration.waiting_for_phone, F.text == "/phone")
async def ask_phone(message: Message):
    await message.answer("Нажми кнопку, чтобы отправить номер телефона:", reply_markup=kb_phone)


@router.message(Registration.waiting_for_phone, F.contact)
async def got_phone(message: Message, state: FSMContext) -> None:
    contact = message.contact
    user = message.from_user

    if not contact or not user:
        return

    if contact.user_id != user.id:
        await message.answer("Пожалуйста, отправь *свой* номер через кнопку.")
        return

    data = await state.get_data()
    token = data.get("verification_token")
    if not token:
        return
    verified = await verify_account(token=token, phone_number=contact.phone_number)
    if not verified:
        await message.answer("Ваш номер телефона не соответствует")
        return

    result = await complete_verify(token=token)
    if result:
        await message.answer("Вы успешно подтвердили номер телефона!")
    else:
        await message.answer("Произошла ошибка. Попробуйте позже.")
    await state.clear()

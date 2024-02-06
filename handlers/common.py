from aiogram import Router
from aiogram.types import Message

from aiogram.utils.markdown import hbold

from aiogram.filters import CommandStart
from helpers.make_keyboard import make_row_keyboard

from comands import address_keyboard

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        text=f"Привіт, {hbold(message.from_user.full_name)}!\nЯ буду допомогати тобі рахувати вартість камунальних послуг.",
        reply_markup=make_row_keyboard(address_keyboard)
    )


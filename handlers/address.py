from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, StartMode

from aiogram.filters.state import State, StatesGroup
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from helpers.make_keyboard import make_row_keyboard


from handlers.services import ServiceDialog
from comands import address_keyboard, yes_no


router = Router()


class AddressState(StatesGroup):
    address_title = State()
    restart_address_title = State()


@router.message(StateFilter(None), F.text.in_(address_keyboard))
async def run_add_address(message: Message, state: FSMContext):
    if message.text == address_keyboard[0]:
        await message.answer('Введіть назву для адреси:')
        await state.set_state(AddressState.address_title)
    elif message.text == address_keyboard[1]:
        await message.answer('Оберай: (TODO додати список)')


@router.message(AddressState.restart_address_title,  F.text.in_(yes_no))
async def create_addres(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == yes_no[0]:
        await state.set_data({})
        await state.set_state(AddressState.address_title)
        await message.answer('Введіть назву для адреси:')

    elif message.text == yes_no[1]:
        # TODO show list
        await message.answer(
            text=f'Добре, вертаємось на головну',
            reply_markup=make_row_keyboard(address_keyboard)
        )
        await state.clear()


@router.message(AddressState.address_title,  F.text.in_(yes_no))
async def confirm_create_addres(message: Message, state: FSMContext, dialog_manager: DialogManager):
    data = await state.get_data()
    if message.text == yes_no[0]:
        await message.answer(text=f'Адреса "{data["address_title"]}" створена!\nЗараз оберіть які лічильники ви бажаєте додати', reply_markup=ReplyKeyboardRemove())
        await dialog_manager.start(ServiceDialog.choosing_services, mode=StartMode.RESET_STACK)

        await state.clear()
        # TODO додати кнопку с листом адрес
    elif message.text == yes_no[1]:
        await message.answer(
            text=f'Створеня адреси "{data["address_title"]}" - Відхилено!\n Бажаєте створити іншу адресу?'
        )
        await state.set_state(AddressState.restart_address_title)


@router.message(AddressState.address_title)
async def validate_create_address(message: Message, state: FSMContext):
    await state.update_data(address_title=message.text)
    await message.answer(
        text=f'Ви дійсно бажаєти створити адресу: "{message.text}"?',
        reply_markup=make_row_keyboard(yes_no)
    )

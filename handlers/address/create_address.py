from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, StartMode

from aiogram.filters.state import State, StatesGroup
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from helpers.make_keyboard import make_row_keyboard, make_colum_keyboard

from database.services import add_address, get_addresses, get_address

from handlers.services import ServiceDialog
from helpers.comands import address_keyboard, yes_no


router = Router(name='create_address')


class AddressState(StatesGroup):
    address_title = State()
    restart_address_title = State()
    choice_address = State()
    chosen_address = State()


@router.message(StateFilter(None), F.text.in_(address_keyboard))
async def run_create_address(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id

        if message.text == address_keyboard[0]:
            await message.answer('Введіть назву для адреси:')
            await state.set_state(AddressState.address_title)
        elif message.text == address_keyboard[1]:
            addresses = await get_addresses(user_id)
            buttons_list = [item[1] for item in addresses]

            await state.set_state(AddressState.choose_address)
            await message.answer(
                text='Оберай адресу:',
                reply_markup=make_colum_keyboard(buttons_list)
            )
    except:
        print("[run_create_address] Something else went wrong")


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
    try:
        data = await state.get_data()
        address = data["address_title"].strip()

        if message.text == yes_no[0]:
            user_id = message.from_user.id
            await add_address(user_id, address)

            await message.answer(text=f'Адреса "{address}" створена!\nЗараз оберіть які лічильники ви бажаєте додати', reply_markup=ReplyKeyboardRemove())
            await dialog_manager.start(ServiceDialog.choosing_services, mode=StartMode.RESET_STACK)

            await state.clear()
            # TODO додати кнопку с листом адрес
        elif message.text == yes_no[1]:
            await message.answer(
                text=f'Створеня адреси "{address}" - Відхилено!\n Бажаєте створити іншу адресу?'
            )
            await state.set_state(AddressState.restart_address_title)
    except:
        print("[confirm_create_addres] Something else went wrong")


@router.message(AddressState.address_title)
async def validate_create_address(message: Message, state: FSMContext):
    await state.update_data(address_title=message.text)
    await message.answer(
        text=f'Ви дійсно бажаєти створити адресу: "{message.text}"?',
        reply_markup=make_row_keyboard(yes_no)
    )


@router.message(AddressState.choice_address)
async def choice_address(message: Message,  state: FSMContext):
    user_id = message.from_user.id
    selected_address_name = message.text

    address = await get_address(user_id, selected_address_name)
    state.update_data(chosen_address=address)

    print('[choice_address|address] -----------------------------')
    print(address)
    # TODO: start readings flow (list: ['add readings', 'show readings', 'calculate -> ["month", "year", "range"]'])

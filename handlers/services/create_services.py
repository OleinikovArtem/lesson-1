from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Multiselect, Button
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.manager.manager import DialogManager

from aiogram.types import CallbackQuery
from aiogram.filters.state import State, StatesGroup


import operator

from helpers.make_keyboard import make_row_keyboard
from helpers.comands import address_keyboard


class ServiceDialog(StatesGroup):
    choosing_services = State()


async def get_data(**kwargs):
    services = [
        ("Світло", '1'),
        ("Газ", '2'),
        ("Вода", '3'),
    ]
    return {
        "services": services,
        "count": len(services),
    }


async def on_services_selected(c: CallbackQuery, button: Button, manager: DialogManager, item_id: str):
    context = manager.current_context()
    selected_services = context.widget_data.get("m_services", [])

    data = await get_data()

    selected_services_ids = [item[0] for item in selected_services]
    services = []

    for id in selected_services_ids:
        for service in data['services']:
            if service[1] == id:
                services.append(service[0])


async def on_finish_selected(c: CallbackQuery, button: Button, manager: DialogManager):
    context = manager.current_context()
    selected_services = context.widget_data.get("m_services", [])

    data = await get_data()

    # Формування відповіді з переліком обраних послуг
    if selected_services:
        selected_services_names = [service[0] for service in data["services"] if service[1] in selected_services]
        response_text = "Ви обрали: " + ", ".join(selected_services_names)
    else:
        response_text = "Ви не обрали жодної послуги."

    await c.message.answer(response_text, reply_markup=make_row_keyboard(address_keyboard))
    await manager.done()  # Завершення діалогу

# Додавання кнопки "Готово" до вікна діалогу
finish_btn = Button(Const("Готово"), id="finish", on_click=on_finish_selected)

services_kbd = Multiselect(
    Format("✓ {item[0]}"),
    Format("{item[0]}"),
    id="m_services",
    item_id_getter=operator.itemgetter(1),
    items="services",
    on_state_changed=on_services_selected,
    min_selected=1,
)


dialog = Dialog(
    Window(
        Const("Послуги:"),
        services_kbd,
        finish_btn,
        state=ServiceDialog.choosing_services,
        getter=get_data,
    ),
)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True, one_time_keyboard=True)


def make_colum_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    colum = [[KeyboardButton(text=item)] for item in items]
    return ReplyKeyboardMarkup(keyboard=colum, resize_keyboard=True, one_time_keyboard=True)

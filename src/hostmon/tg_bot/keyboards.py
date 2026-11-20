from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить сайт"),
            KeyboardButton(text="Удалить сайт"),
        ]
    ],
    resize_keyboard=True,
    is_persistent=True,
)

import textwrap

from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import textwrap

from aiogram.types import Message

from hostmon.tg_bot.keyboards import main_keyboard

_DATE_FORMAT = "%d.%m.%Y"
main_router = Router()


@main_router.message(Command("start"))
async def main_menu(message: Message) -> None:
    msg = textwrap.dedent(
        "🌟Добро пожаловать! "
        "Вы можете добавить сайт, мы добавим монитор на этот сайт и будем проверять, "
        "если вдруг с ними что то будет не так, мы оповестим вас!"
    )

    await message.answer(msg, reply_markup=main_keyboard)

@main_router.message(F.text.startswith("Добавить сайт"))
async def unknown_command(message: Message) -> None:
    await message.answer("Упс, я не знаю такой команды", reply_markup=main_keyboard)

@main_router.message(F.text.startswith("Удалить сайт"))
async def unknown_command(message: Message) -> None:
    await message.answer("Упс, я не знаю такой команды", reply_markup=main_keyboard)


@main_router.message(F.text.startswith("/"))
async def unknown_command(message: Message) -> None:
    await message.answer("Упс, я не знаю такой команды", reply_markup=main_keyboard)


@main_router.message(F.text)
async def answer_default_message(message: Message) -> None:
    await message.answer(
        "😅 Извините, я пока не понимаю эту команду. "
        "Попробуйте выбрать что-то из меню или напишите иначе.",
    )


@main_router.message(F.content_type)
async def answer_default_file(message: Message) -> None:
    await message.answer(
        "😅Ой! Я не умею работать с файлами.",
    )

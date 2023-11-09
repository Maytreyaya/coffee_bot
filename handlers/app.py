from aiogram import Router, F, types
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message(Command('app'))
async def app(message: Message):
    but = types.KeyboardButton(text="Open the page", web_app=WebAppInfo(url="https://fastapi.tiangolo.com/tutorial/body/"))

    markup = types.ReplyKeyboardMarkup(keyboard=[but], resize_keyboard=True)
    await message.answer("Hello!", reply_markup=markup)
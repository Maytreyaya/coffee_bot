import asyncio
import logging

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from contextlib import suppress
from datetime import datetime
from typing import Optional
from aiogram import html
from aiogram import Bot, Dispatcher, types
from aiogram.enums import DiceEmoji
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.filters.command import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from magic_filter import F
from handlers import orders


from config_reader import config

#
# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     kb = [
#         [types.KeyboardButton(text="Espresso")],
#         [types.KeyboardButton(text="Doppio")],
#         [types.KeyboardButton(text="Latte")],
#         [types.KeyboardButton(text="Capuccino")],
#     ]
#     keyboard = types.ReplyKeyboardMarkup(
#         keyboard=kb,
#         resize_keyboard=True,
#         input_field_placeholder="Choose your drink"
#     )
#     await message.answer("Welcome to our web coffe shop,"
#                          " here you can make your order."
#                          " What drink you you would like to have?",
#                          reply_markup=keyboard)
#
#
# @dp.message(Command("test1"))
# async def cmd_test1(message: types.Message):
#     await message.reply("Test 1")
#
#
# @dp.message(Command("dice"))
# async def cmd_dice(message: types.Message, bot: Bot):
#     await bot.send_dice(message.chat.id, emoji=DiceEmoji.DICE)
#
#
# user_data = {}
#
#
# class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
#     action: str
#     value: Optional[int] = None
#
#
# def get_keyboard():
#     # buttons = [
#     #     [
#     #         types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
#     #         types.InlineKeyboardButton(text="+1", callback_data="num_incr")
#     #     ],
#     #     [types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")]
#     # ]
#     # keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
#     # return keyboard
#     builder = InlineKeyboardBuilder()
#     builder.button(
#         text="1", callback_data=NumbersCallbackFactory(action="change", value=1)
#     )
#     builder.button(
#         text="2", callback_data=NumbersCallbackFactory(action="change", value=2)
#     )
#     builder.button(
#         text="3", callback_data=NumbersCallbackFactory(action="change", value=3)
#     )
#     builder.button(
#         text="4", callback_data=NumbersCallbackFactory(action="change", value=4)
#     )
#     builder.button(
#         text="Подтвердить", callback_data=NumbersCallbackFactory(action="finish")
#     )
#     # Выравниваем кнопки по 4 в ряд, чтобы получилось 4 + 1
#     builder.adjust(4)
#     return builder.as_markup()
#
#
# async def update_num_text(message: types.Message, new_value: int):
#     with suppress(TelegramBadRequest):
#         await message.edit_text(
#             f"Укажите число: {new_value}",
#             reply_markup=get_keyboard()
#         )
#
#
# @dp.message(lambda message: message.text.lower() in ["espresso", "doppio", "latte", "capuccino"])
# async def cmd_numbers(message: types.Message):
#     user_data[message.from_user.id] = 0
#     await message.answer("Укажите число: 0", reply_markup=get_keyboard())
#
#
# @dp.callback_query(NumbersCallbackFactory.filter())
# async def callbacks_num_change_fab(
#         callback: types.CallbackQuery,
#         callback_data: NumbersCallbackFactory
# ):
#     # Текущее значение
#     user_value = user_data.get(callback.from_user.id, 0)
#     # Если число нужно изменить
#     if callback_data.action == "change":
#         user_data[callback.from_user.id] = callback_data.value
#         await update_num_text(callback.message, callback_data.value)
#     # Если число нужно зафиксировать
#     else:
#         await callback.message.edit_text(f"Итого: {user_value}")
#     await callback.answer()
#
# #
# # @dp.callback_query(F.data.startswith("num_"))
# # async def callbacks_num(callback: types.CallbackQuery):
# #     user_value = user_data.get(callback.from_user.id, 0)
# #     action = callback.data.split("_")[1]
# #
# #     if action == "incr":
# #         user_data[callback.from_user.id] = user_value+1
# #         await update_num_text(callback.message, user_value+1)
# #     elif action == "decr":
# #         user_data[callback.from_user.id] = user_value-1
# #         await update_num_text(callback.message, user_value-1)
# #     elif action == "finish":
# #         await callback.message.edit_text(f"Итого: {user_value}")
# #
# #     await callback.answer()
#
#
# @dp.message(Command("name"))
# async def cmd_name(message: types.Message, command: CommandObject):
#     if command.args:
#         await message.answer(f"Привет, {html.bold(html.quote(command.args))}", parse_mode="HTML")
#     else:
#         await message.answer("Пожалуйста, укажи своё имя после команды /name!")
#
#
# @dp.message(F.text)
# async def echo_with_time(message: types.Message):
#     # Получаем текущее время в часовом поясе ПК
#     time_now = datetime.now().strftime('%H:%M')
#     # Создаём подчёркнутый текст
#     added_text = html.underline(f"Создано в {time_now}")
#     # Отправляем новое сообщение с добавленным текстом
#     await message.answer(f"{message.text}\n\n{added_text}", parse_mode="HTML")


async def main():

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config.bot_token.get_secret_value())

    dp = Dispatcher()

    dp.include_routers(orders.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

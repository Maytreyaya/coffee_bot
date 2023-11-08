import sqlite3

from aiogram import Router, F, types
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

name = None
password = None


class Form(StatesGroup):
    username = State()
    password = State()


@router.message(Command("register"))
async def register(message: Message, state: FSMContext):
    conn = sqlite3.connect("coffee.sql")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))")
    conn.commit()
    cursor.close()
    conn.close()
    await message.answer("Let's register! Provide your name!")
    await state.set_state(Form.username)


@router.message(Form.username)
async def username(message: Message, state: FSMContext):
    global name
    global password

    name = message.text.strip()
    await state.set_state(Form.password)
    await message.answer("Password please")


@router.message(Form.password)
async def passwordd(message: Message, state: FSMContext):
    global password
    password = message.text.strip()

    conn = sqlite3.connect("coffee.sql")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))

    conn.commit()
    cursor.close()
    conn.close()

    markup = InlineKeyboardBuilder()
    markup.row(types.InlineKeyboardButton(text='Users: ', callback_data='users'))


    await message.answer("User registered", reply_markup=markup.as_markup())
    await state.clear()


@router.callback_query(F.data == "users")
async def callback(message: Message):

    conn = sqlite3.connect("coffee.sql")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    info = ''
    for el in users:
        info += f'Name: {el[1]}\n'

    cursor.close()
    conn.close()

    await message.answer(info)
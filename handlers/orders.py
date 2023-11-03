from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

router = Router()


class OrderFood(StatesGroup):
    choosing_drink_name = State()
    choosing_drink_size = State()
    choosing_desert_desire = State()
    choosing_food_name = State()


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Making reply keyboard
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


available_drinks_names = ["Espresso", "Doppio", "Latte", "Capuccino"]
available_drinks_sizes = ["Small", "Big"]
available_food_names = ["Cake", "Cookie", "Brownie"]
reply = ["Yes", "No"]


@router.message(StateFilter(None), Command("order"))
async def cmd_order(message: Message, state: FSMContext):
    await message.answer(
        text="Choose your drink, please",
        reply_markup=make_row_keyboard(available_drinks_names)
    )
    await state.set_state(OrderFood.choosing_drink_name)


@router.message(
    OrderFood.choosing_drink_name,
    F.text.in_(available_drinks_names)
)
async def drink_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_drink=message.text.lower())
    await message.answer(
        text="Thank you, Now choose the size:",
        reply_markup=make_row_keyboard(available_drinks_sizes)
    )
    await state.set_state(OrderFood.choosing_drink_size)


@router.message(OrderFood.choosing_drink_name)
async def drink_chosen_incorrectly(message: Message):
    await message.answer(
        text="there is no such drink, please choose below:",
        reply_markup=make_row_keyboard(available_food_names)
    )


@router.message(
    OrderFood.choosing_drink_size,
    F.text.in_(available_drinks_sizes)
)
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_drink_size=message.text.lower())
    await message.answer(
        text="Thank you, would you like to have dessert?",
        reply_markup=make_row_keyboard(reply)
    )
    await state.set_state(OrderFood.choosing_desert_desire)


@router.message(
    OrderFood.choosing_desert_desire,
    F.text.in_(["yes", "Yes"])
)
async def desire_chosen(message: Message, state: FSMContext):
    await message.answer(
        text="Super! Please choose your desert!",
        reply_markup=make_row_keyboard(available_food_names)
    )
    await state.set_state(OrderFood.choosing_food_name)


@router.message(
    OrderFood.choosing_desert_desire,
    F.text.in_(["no", "No"])
)
async def desire_chosen(message: Message, state: FSMContext):
    await message.answer(
        text="Okay, let's move forward!",
        reply_markup=make_row_keyboard("Finish order")
    )
    user_data = await state.get_data()
    await message.answer(
        text=f" ~Your order~ : {user_data['chosen_drink_size'].capitalize()} {user_data['chosen_drink'].capitalize()}",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(OrderFood.choosing_food_name, F.text.in_(available_food_names))
async def food_size_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f" ~Your order~ : {user_data['chosen_drink_size'].capitalize()} {user_data['chosen_drink'].capitalize()}"
             f" and {user_data['chosen_food'].capitalize()}",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()

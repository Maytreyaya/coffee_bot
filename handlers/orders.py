from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

router = Router()


class OrderFood(StatesGroup):
    choosing_drink_name = State()
    choosing_drink_size = State()
    choosing_quantity = State()
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
quantity = ["1", "2", "3", "4", "5", "6", "7", "8"]


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

@router.message(
    OrderFood.choosing_drink_size,
    F.text.in_(available_drinks_sizes)
)
async def drink_size_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_drink_size=message.text.lower())
    await message.answer(
        text="Thank you, Now choose quantity:",
        reply_markup=make_row_keyboard(quantity)
    )
    await state.set_state(OrderFood.choosing_quantity)


@router.message(
    OrderFood.choosing_quantity,
    F.text.in_(quantity)
)
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_quantity=message.text.lower())

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
        reply_markup="Finish order"
    )
    user_data = await state.get_data()
    await message.answer(
        text=f" ~Your order~ : {user_data['chosen_quantity']}"
             f" {user_data['chosen_drink_size'].capitalize()}"
             f" {user_data['chosen_drink'].capitalize()}",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()


@router.message(OrderFood.choosing_food_name, F.text.in_(available_food_names))
async def food_size_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f" ~Your order~ : {user_data['chosen_quantity']}"
             f" {user_data['chosen_drink_size'].capitalize()}"
             f" {user_data['chosen_drink'].capitalize()}"
             f" and {user_data['chosen_food'].capitalize()}",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()

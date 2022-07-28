"""

    name: telegram-todo
    date: 28.07.22
    creator: HellenWeb
    github: https://github.com/HellenWeb/telegram-todo

"""

# Modules

import os
import sys

try:
    from dispacher import bot, dp, db
    from aiogram import types, executor
    from aiogram.dispatcher import FSMContext
    from aiogram.dispatcher.filters.state import State, StatesGroup
except ModuleNotFoundError:
    os.system("pip3 install aiogram loguru requests")
    os.system("pip3 freeze")
    sys.exit(1)

# Logic

"""

    States

"""


class FSMSettings(StatesGroup):
    task = State()


@dp.message_handler(state=FSMSettings.task)
async def added_task(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["task"] = message.text
    await message.answer("Task saved")
    db.add_task(message.from_user.id, data["task"])
    await state.finish()


"""Welcome"""


@dp.message_handler(commands=["start"])
async def echo(message: types.Message):
    mark = types.InlineKeyboardMarkup(row_width=True)
    mark.row(types.InlineKeyboardButton(text="❓", callback_data="help"))
    await message.answer(
        f"<strong>Hello</strong> {message.from_user.first_name} 😀\n\n<strong>- This bot will help you manage your time properly and improve you</strong>\n\nCreator: @YungHellen",
        reply_markup=mark,
    )


@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.answer(
        "<strong>/start</strong> - Welcome message\n<strong>/help</strong> - All commands\n<strong>/tasks</strong> - List your tasks"
    )


@dp.message_handler(commands=["tasks"])
async def tasks(message: types.Message):
    mark = types.InlineKeyboardMarkup(row_width=True)
    for i in db.show_tasks(message.from_user.id):
        mark.row(
            types.InlineKeyboardButton(text="❌", callback_data=f"delete {i[2]}"),
            types.InlineKeyboardButton(text=i[2], callback_data=f"callback {i[2]}"),
            types.InlineKeyboardButton(text=i[3], callback_data=f"date {i[3]}"),
        )
    mark.add(types.InlineKeyboardButton(text="➕ (Add Task)", callback_data="add_task"))
    await message.answer("Tasks:", reply_markup=mark)


@dp.callback_query_handler(lambda r: True)
async def callbacks(c: types.CallbackQuery):
    if c.data == "help":
        mark = types.InlineKeyboardMarkup(row_width=True)
        mark.row(types.InlineKeyboardButton(text="⬅️", callback_data="back"))
        await bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="<strong>/start</strong> - Welcome message\n<strong>/help</strong> - All commands\n<strong>/tasks</strong> - List your tasks",
            reply_markup=mark,
        )
    if c.data == "back":
        mark1 = types.InlineKeyboardMarkup(row_width=True)
        mark1.row(types.InlineKeyboardButton(text="❓", callback_data="help"))
        await bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=f"<strong>Hello</strong> {c.from_user.first_name} 😀\n\n<strong>- This bot will help you manage your time properly and improve you</strong>\n\nCreator: @YungHellen",
            reply_markup=mark1,
        )
    if c.data == "add_task":
        await FSMSettings.task.set()
        await c.message.answer("Enter your task")
    for i in db.show_tasks(c.from_user.id):
        if c.data == f"delete {i[2]}":
            db.delete_task(c.from_user.id, i[2])
            await c.message.answer("Your task successfully deleted ✅")
        if c.data == f"callback {i[2]}":
            mark = types.InlineKeyboardMarkup(row_width=True)
            mark.add(types.InlineKeyboardButton(text="❌", callback_data="msg_delete"))
            await c.message.answer(
                f"Name: <strong>{i[2]}</strong>\nDate: <strong>{i[3]}</strong>",
                reply_markup=mark,
            )
        if c.data == f"date {i[3]}":
            mark = types.InlineKeyboardMarkup(row_width=True)
            mark.add(types.InlineKeyboardButton(text="❌", callback_data="msg_delete"))
            await c.message.answer(
                f"Name: <strong>{i[2]}</strong>\nDate: <strong>{i[3]}</strong>",
                reply_markup=mark,
            )
    if c.data == "msg_delete":
        await c.message.delete()


# Polling

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

from aiogram import types

button_outside_warning_y = "yes"
button_outside_warning_n = "no"

confirm_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_y = types.KeyboardButton(button_outside_warning_y)
button_n = types.KeyboardButton(button_outside_warning_n)
confirm_keyboard.add(button_n)
confirm_keyboard.add(button_y)
from aiogram import types


button_location_name = "Send my location"
location_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = types.KeyboardButton(button_location_name, request_location=True)
location_kb.add(button_1)
import datetime
import traceback

import app.dbwork.db2Working
import app.converters.street_converter
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from app.dbwork.dbInit import db_handler as sql_handler
from app.keyboards.confirm_kb import confirm_keyboard, button_outside_warning_y, button_outside_warning_n
from app.keyboards.location_kb import button_location_name, location_kb

outside_warning_msg = "✍🏼❓ Are you sure that you want to make changes in your personal information?"

button_outside_warning_send_message = "✍🏼✔ Thank you for updating the data by actual information"

UPDATE_MESSAGE = "✍🏼 Using this command you can change your personal information in particular you location information"

PARTICIPATING_MESSAGE = "✔ GOOD! You are participating in next poll"

WRONG_MESSAGE = "⚠ Something went wrong..."

CANT_FIND_CITY_MESSAGE = "🗺️❓ Cant find the city by following coordinates, are you sure that you are standing in one" \
                         " that " \
                         "supports this functionality? "

CANT_DELETE_MESSAGE_ERR = "♻This message can`t be deleted as it was sent more than 2 days ago but you mast be " \
                          "participating in the poll "

NOT_SAVED_CHANGES_MESSAGE = "✍🏼❌ Your changes are have not been saved"

NEXT_DELIVERING_MESSAGE = "🕒 Using this command you can get informed about the next arriving of aid trucks.\
 The next delivery of humanitarian assistance will be at :"

CONFIRMATION_MESSAGE = "✔ Please type \"Yes\" or \"No\" or click the button"

YES = "yes"

NO = "no"

LNG = "longt"

LAT = "latit"


class StarterInitialize(StatesGroup):
    waiting_for_starter_location = State()


class SendLocation(StatesGroup):
    waiting_for_location = State()
    waiting_for_message = State()
    waiting_for_polling = State()


async def location_confirmed(message: types.Message, state: FSMContext):
    if message.location is None:
        await message.answer("please click on the button\"{}\"".format(button_location_name))
        return
    await state.update_data(longt=message.location.longitude, latit=message.location.latitude)

    await message.answer(outside_warning_msg, reply_markup=confirm_keyboard)
    await SendLocation.next()


async def warning_confirmed(message: types.Message, state: FSMContext):
    if message.text.lower() not in [YES, NO, button_outside_warning_y, button_outside_warning_n]:
        await message.answer(CONFIRMATION_MESSAGE)
        return
    else:
        if message.text.lower().__eq__(NO):
            await SendLocation.next()
            await message.answer(NOT_SAVED_CHANGES_MESSAGE, reply_markup=types.ReplyKeyboardRemove())
            return
        else:
            user_data = await state.get_data()
            lat = user_data.get(LAT)
            lon = user_data.get(LNG)
            try:
                city = app.converters.street_converter.convert_street(lat, lon)
                await sql_handler.insert_or_update_user_info(lon=lon, lat=lat, chat_id=message.chat.id, city=city)
            except AttributeError as atr:
                await message.answer(CANT_FIND_CITY_MESSAGE)
                return
            except Exception:
                await message.answer(CANT_FIND_CITY_MESSAGE)
                print(traceback.format_exc())
                return
    await state.update_data(confirmed_user=True)
    await message.answer(button_outside_warning_send_message, reply_markup=types.ReplyKeyboardRemove())
    await SendLocation.next()


async def polling_confirmation_successful(callback: types.CallbackQuery, state: FSMContext):
    try:
        await sql_handler.insert_or_update_participating(callback.message.chat.id)
        diff = callback.message.date - (datetime.datetime.now() - datetime.timedelta(days=2))
        if diff.total_seconds() < 0:
            await callback.message.edit_reply_markup(reply_markup=None)
            await callback.message.edit_text(
                text=CANT_FIND_CITY_MESSAGE)
            await callback.message.answer(PARTICIPATING_MESSAGE)
        else:
            await callback.message.delete()
            await callback.message.answer(PARTICIPATING_MESSAGE)
    except Exception:
        await callback.message.answer(WRONG_MESSAGE)


async def get_time_of_receiving(message: types.Message, state: FSMContext):
    try:
        res = await sql_handler.get_time_of_city(message.chat.id)
        await message.answer(text=NEXT_DELIVERING_MESSAGE + " " + res.strftime("%Y.%m.%d, %H:%M"))
    except Exception as arg:
        print("exception ", arg)
        await message.answer(WRONG_MESSAGE)


def register_handlers_find_loc(dp1: Dispatcher):
    dp1.register_message_handler(start_application, state="*", commands="update_personal")
    dp1.register_message_handler(location_confirmed, content_types=['location'],
                                 state=SendLocation.waiting_for_location)
    dp1.register_message_handler(location_confirmed, state=SendLocation.waiting_for_location)
    dp1.register_message_handler(warning_confirmed, state=SendLocation.waiting_for_message)
    dp1.register_message_handler(get_time_of_receiving, state=SendLocation.waiting_for_polling, commands="time")
    dp1.register_callback_query_handler(polling_confirmation_successful, state=SendLocation.waiting_for_polling)


@dp.message_handler(commands=['update_personal'])
async def start_application(message: types.Message):
    await message.reply(UPDATE_MESSAGE, reply_markup=location_kb)
    await SendLocation.waiting_for_location.set()

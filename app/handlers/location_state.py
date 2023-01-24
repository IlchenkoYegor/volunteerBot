import traceback

import app.dbwork.db2Working
import app.converters.street_converter
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from app.middleware.throttle import ThrottlingMiddleware, rate_limit
from app.dbwork.dbInit import db_handler as sql_handler
from app.keyboards.confirm_kb import confirm_keyboard, button_outside_warning_y, button_outside_warning_n
from app.keyboards.location_kb import button_location_name, location_kb

outside_warning_msg = "Are you sure that you want to make changes in your personal information?"

button_outside_warning_send_message = "Thank you for updating the data by actual information"

UPDATE_MESSAGE = "Using this command you can change your personal information in particular you location information"

PARTICIPATING_MESSAGE = "GOOD! You are participating in next poll"

WRONG_MESSAGE = "Something went wrong..."

CANT_FIND_CITY_MESSAGE = "cant find the city by following coordinates, are you sure that you are standing in one that supports this functionallity?"

NOT_SAVED_CHANGES_MESSAGE = "your changes are have not been saved"
   # "Ви користуєтеся ботом для надання додаткової інформації про місцезнаходження,"
   #                     " будьте відповідальні! Для продовження натисніть на кнопку \"Відправити свою локацію\" і "
   #                     "відправте свою геолокацію або виберіть її вручну (при вимкненому місцеположенні)."
   #                     " Дозволено 1 запит в 3 хвилини від початку введення команди"


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
    if message.text.lower() not in ["yes", "no", button_outside_warning_y, button_outside_warning_n]:
        await message.answer("Please type \"Yes\" or \"No\" or click the button")
        return
    else:
        if(message.text.lower().__eq__("no")):
            await SendLocation.next()
            await message.answer(NOT_SAVED_CHANGES_MESSAGE, reply_markup=types.ReplyKeyboardRemove())
            return
        else:
            user_data = await state.get_data()
            lat = user_data.get('latit')
            lon = user_data.get('longt')
            try:
                city = app.converters.street_converter.convert_street(lat, lon)
                await sql_handler.insert_or_update_user_info(lon=lon, lat=lat, chat_id=message.chat.id,city= city)
                print(message.chat.id)
            except AttributeError as atr:
                await message.answer(atr.name)
                return
            except Exception:
                await message.answer(CANT_FIND_CITY_MESSAGE)
                print(traceback.format_exc())
                return
    #await state.update_data(confirm=message.text)
    await message.answer(button_outside_warning_send_message, reply_markup=types.ReplyKeyboardRemove())
    await SendLocation.next()


async def polling_confirmation_successful(callback: types.CallbackQuery,  state: FSMContext):
    await callback.message.answer(PARTICIPATING_MESSAGE)
    try:
        await sql_handler.insert_or_update_participating(callback.message.chat.id)
    except Exception:
        await callback.message.answer(WRONG_MESSAGE)
    await callback.message.delete()


def register_handlers_find_loc(dp1: Dispatcher):
    dp1.middleware.setup(ThrottlingMiddleware())
    dp1.register_message_handler(start_application, commands="start_locate", state="*")
    dp1.register_message_handler(location_confirmed, content_types=['location'], state=SendLocation.waiting_for_location)
    dp1.register_message_handler(location_confirmed, state=SendLocation.waiting_for_location)
    dp1.register_message_handler(warning_confirmed,  state=SendLocation.waiting_for_message)
    dp1.register_callback_query_handler(polling_confirmation_successful, state=SendLocation.waiting_for_polling) #commands="/participateInPoll")
    #dp1.register_message_handler(text_sent, state=SendLocation.waiting_for_message)


# async def text_sent(message: types.Message, state: FSMContext):
#     if len(message.text) < 6 or len(message.text) > 400:
#         await message.answer("Будьте ласкаві, напишіть повідомлення більше 6 і менше 400 символів")
#         return
#     user_data = await state.get_data()
#     lat = user_data.get('latit')
#     lon = user_data.get('longt')
#     war_s = True
#     address, region = app.converters.street_converter.convert_street(lat, lon)
#     message_f = message.text
#     await state.finish()
#     try:
#         await sql_handler.insert_new_data(lon, lat, war_s, message_f, address, region)
#         await message.answer("Дякуємо за інформацію, ваше повідомлення було збережено", reply_markup=types.ReplyKeyboardRemove())
#     except:
#         await message.answer("Помилка в визначенні локації, запит не був збережений (запит можливий в межах України)", reply_markup=types.ReplyKeyboardRemove())

#@rate_limit(180, 'update_locate')
@dp.message_handler(commands=['update_personal'])
async def start_application(message: types.Message):
    await message.reply(UPDATE_MESSAGE, reply_markup=location_kb)
    await SendLocation.waiting_for_location.set()
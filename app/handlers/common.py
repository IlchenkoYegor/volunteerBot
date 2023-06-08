from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from . import location_state


STARTING_MESSAGE = "👋🏼 You are using the bot which helps to find the most fitting points of providing humanitarian \
aid, type \"/update_personal\" to configure your personal data and to start to recieve messages of polling"

CONFIRMED_USER = 'confirmed_user'

CANT_CANCEL_MSG = "❗ Can`t stop actions on the first registration, make sure "\
                                 "you have entered the location data or if you change your mind"\
                                 " and don`t want to participate in the polls you can leave this chat"

async def cmd_start(message: types.Message, state: FSMContext):
    if(await state.get_data()).get(CONFIRMED_USER) is None:
        await state.finish()
        await message.answer(STARTING_MESSAGE
        )
    else:
        return


async def cmd_cancel(message: types.Message, state: FSMContext):
    if await state.get_state() != None:
        if(await state.get_data()).get(CONFIRMED_USER) is not None:
            await state.set_state(await location_state.SendLocation.last())
        else:
            await message.answer(CANT_CANCEL_MSG)
            return
    else:
        return
    await message.answer("❗️Actions stopped", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
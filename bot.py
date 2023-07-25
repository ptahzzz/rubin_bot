from comand_file import *
from lists import *
import random
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from config import token

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    znak = State()
    birth = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["библиотека песен", "песенник"]
    keyboard.add(*buttons)
    buttons = ["кто я по зз", "кто я по дню рождения", "библиотека аккордов"]
    keyboard.add(*buttons)
    await message.answer("Привет, меня зовут Коко! \nВсё, что я умею, ты можешь найти, написав /help", reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer("  Если ты хочешь узнать песни в моей библиотеке, то напиши команду 'библиотека песен' или нажми"
                         " соответствующую кнопку.\n"
                         "  Если ты хочешь увидеть текст и аккорды песни из моей библиотеки, то просто напиши"
                         " её название, как в библиотеке\n"
                         "  Если ты несчасный гитарист, который забыл аккорды, то просто напиши 'библиотека аккордов',"
                         " или нажми соответствующую кнопку\n"
                         "  Чтобы не искать песенник по всем беседам, просто напиши команду 'песенник' или нажми "
                         "соответствующую кнопку\n"
                         "  Если ты хочешь узнать, какой ты комиссар по знаку зодиака, то напиши команду 'кто я по зз' "
                         "или нажми на соответсвующую кнопку. Затем следуй моим указаниям.\n"
                         "  Если ты хочешь узнать, какой ты комиссар по дню рождения, то напиши команду 'кто я по дню рождения' "
                         "или нажми на соответсвующую кнопку. Затем следуй моим указаниям.")


@dp.message_handler(Text(equals="библиотека песен"))
async def song_list(message: types.Message):
    await message.answer('\n'.join(list_song))


@dp.message_handler(Text(equals="библиотека аккордов"))
async def accord_def(message: types.Message):
    photo = open(' songs/according.png', 'rb')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)


@dp.message_handler(Text(equals="песенник"))
async def song_rub(message: types.Message):
    await message.answer_document(open('Песни Рубина.pdf', 'rb'))


@dp.message_handler(Text(equals='кто я по зз'))
async def znak_start_command(message: types.Message):
    await Form.znak.set()
    await message.answer("Введите дату своего рождения, в формате: 'mm.dd'. Например мой создатель родился 26 апреля,"
                         " значит он должен ввести: 04.26 \nТак ты сможешь узнать, какой ты комиссар по знаку зодиака.")


@dp.message_handler(state=Form.znak)
async def znak_command(message: types.Message, state: FSMContext):
    date = message.text.split('.')
    if (len(date) == 2) and (int(date[0]) <= 12) and (int(date[0]) >= 1) and (int(date[1]) <= 31) and (int(date[1]) >= 1):
        znak = converted_date(f'{date[0]}-{date[1]}', False)
        if znak == 'cкорпион':
            await message.answer("К сожалению, среди наших коммисаров нет скорпионов.\n"
                                 "Нам тоже от этого хочется плакать(")
        else:
            comisar = random.choice(list_zod_com[znak])
            comisar = comisar[0]
            photo = open(f'photo/{comisar}.png', 'rb')
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
            await message.answer(f'Вы - {comisar}, {znak.capitalize()}\n'
                                 f'\n'
                                 f'{list_zod_op[znak]}')
    else:
        await message.answer('Дата неверна')

    await state.finish()


@dp.message_handler(Text(equals='кто я по дню рождения'))
async def birth_command_start(message: types.Message):
    await Form.birth.set()
    await message.answer("Введите дату своего рождения, в формате: 'mm.dd'. Например мой создатель родился 26 апреля,"
                         " значит он должен ввести: 04.26 \nТак ты сможешь узнать, какой ты комиссар по дате рождения.")


@dp.message_handler(state=Form.birth)
async def birth_command(message: types.Message, state: FSMContext):
    date = message.text.split('.')
    if (len(date) == 2) and (int(date[0]) <= 12) and (int(date[0]) >= 1) and (int(date[1]) <= 31) and (int(date[1]) >= 1):
        znak = converted_date(f'{date[0]}-{date[1]}', True)
        comis = minimal_razn(znak)
        photo = open(f'photo/{comis}.png', 'rb')
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
        await message.answer(f'Вы - {comis}')
    else:
        await message.answer('Дата неверна')

    await state.finish()




@dp.message_handler()
async def song_text(message: types.Message):
    song = message.text.capitalize()
    if song in list_song:
        await message.answer(music_text(song))
    else:
        await message.answer('Такой песни нет в моей библиотеке, или вы указали её название неверно')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
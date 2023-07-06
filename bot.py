'''
1) Бот не имеет доступа к общим чатам.(Botfather->/setprivicy->Disabled)
'''

import config
import logging

from aiogram import Bot, Dispatcher, executor, types

# FSM CONTEXT
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

#Configure logging
logging.basicConfig(level=logging.INFO)

# Инициализация Бота и Диспетчера
bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Создание класса для Состояний
class Pwd_State(StatesGroup):
    pwd_len = State()

'''################################## KEYBOARDS ##########################################'''
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b_start = KeyboardButton('Начать')
b_generate = KeyboardButton('Сгенерировать пароль')
b_cancel = KeyboardButton('<-- Назад')
b_help = KeyboardButton('Помощь')

kbd1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kbd2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kbd1.insert(b_generate).insert(b_help)
kbd2.add(b_cancel)

# Тест обработчик команд
# all_commands = ['start', 'help', 'generate']
@dp.message_handler(text=['Начать', '/start']) # ++++kbd1
async def start(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, добро пожаловать в бот - 'Генератор Паролей'.\n"
                         "Чтобы сгенерировать пароль, напишите --- /generate",
                         reply_markup=kbd1)
                         
@dp.message_handler(text = ['Помощь', '/help'])
async def help(message: types.Message):
    await message.answer("Для обратной связи напишите на почту koryun0arakel@gmail.com", reply_markup=kbd1)

@dp.message_handler(text=['Сгенерировать пароль', '/generate']) # ++++kbd2
async def generate(message: types.Message):
    await message.answer("Укажите длину пароля:", reply_markup=kbd2)
    await Pwd_State.pwd_len.set()# обрашаемся к классу PwdState, зстем состоянию pwd_len

    # С помощью set() устанавливаем данное состояние. Отныне наш pwd_len имеет state.
# Создадим handler, который будет реагировать только на текущий state()

@dp.message_handler(state='*', text=['<-- Назад', '/cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    #Разрешать пользователю отменять действие с помощью команды /cancel

    current_state = await state.get_state()
    if current_state is None:
        # Пользователь не находится ни в каком состоянии, игнорируем.
        return
    # Cancel действие, и сообщаем об этом пользователью
    await state.finish()
    await message.reply("Чтобы сгенерировать пароль, напишите --- /generate",reply_markup=kbd1)

from password_generator import generate_normal
@dp.message_handler(state=Pwd_State.pwd_len)
async def get_pwd_len(message: types.Message, state: FSMContext):
    num = int(message.text)

    if (num < 8) or (num > 35):
        await message.answer('Длина пароля может состоять из 8 до 35 символов.') # если добавить reply_markup=kbd1, выдаст ошибку!!! Надо исправить
    else:
        await state.update_data(pwd_len=message.text)
        data = await state.get_data()
        pwd_len = int(data['pwd_len'])
        await message.answer(f"{generate_normal(pwd_len)}", reply_markup=kbd1)

        await state.finish()

# run long-polling
if __name__ == '__main__':
    print('Password_Bot Is Ready To Use!!!!')
    executor.start_polling(dp, skip_updates=True)
    executor.stop_polling()
    executor.start_polling()
    #executer.stop_polling()
    #executer.start_polling()
    
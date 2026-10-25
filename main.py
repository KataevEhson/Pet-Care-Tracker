from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from dotenv import load_dotenv 
from service import *
from conection import *
import asyncio
import os



load_dotenv()

token = os.getenv("TOCEN")

bot = Bot(token=token)
dp = Dispatcher()



# main_kb = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="📋 Мои задачи")],
#         [KeyboardButton(text="🆘 Помощь")],
#     ],
#     resize_keyboard=True,
# )




@dp.message(CommandStart())
async def start_my_bot(message : Message):
    await message.answer(f"""
🐾 Привет, {message.from_user.full_name}!

Я помогу заботиться о твоём питомце и помнить о важных делах 🐶🐱

🍽 Кормление
💊 Приём лекарств
💉 Прививки и посещения ветеринара

Давай познакомимся с твоим любимцем! Нажми /add_pat 👇
Или если нужна помощ то нажимай /help
""")




@dp.message(Command("help"))
async def help_user(message : Message):
    try:
        await message.answer("""
Что можно делать?

/add_pet Записывать кормления
/my_pets Отмечать прогулки
/log_care Вести учёт приёма лекарств
/pet_history Сохранять даты прививок
/last_vaccination Записывать вес питомца


Выбери нужный раздел с помощью кнопок меню 
""")
    except Exception as erorr:
        print("Help command erorr:", erorr)


@dp.message(Command("my_pets"))
async def print_my_pets(message : Message):
    petsy = await my_pets(message.from_user.id)
    result = ""
    for i in petsy:
        result += f"""
=== Id {i['id']} ===
Name: {i['name']} 
Species: {i['species']} 
"""
    await message.answer(result)





@dp.message(Command("add_pet"))
async def create_new_pet(messaga : Message, command : CommandObject):
    try:
        example = command.args
        example = example.split("/")
        res = await create_pet(messaga.from_user.id ,example[0], example[1])
        await messaga.answer("Pet create sucessful 👌🏿")
    except:
        print("Ошибка провер что ты мне кинул")







@dp.message(Command("feeding_pet"))
async def feeding_for_me(message : Message, command : CommandObject):
    example = command.args
    await log_care(message.from_user.id, int(example), 'feeding')
    await message.answer("Ваш питомец хорошо покушал 🥩")


@dp.message(Command("vet_visit_pet"))
async def vet_visit_for_me(message : Message, command : CommandObject):
    example1 = command.args
    await log_care(message.from_user.id, int(example1), 'vet_visit')
    await message.answer("Ваш питомец хорошо покушал 🥩")



@dp.message(Command("vaccination_pet"))
async def vaccination_for_me(message : Message, command : CommandObject):
    example2 = command.args

    await log_care(message.from_user.id, int(example2), 'vaccination')
    await message.answer("Ваш питомец хорошо ")











async def main():
    await create_table()
    print("Create table succesifull")
    await dp.start_polling(bot)
    print("Bot started")
    
    
    
if __name__ == "__main__":
    asyncio.run(main())


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



main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🐾 Мои питомцы")],
        [KeyboardButton(text="📋 Добавить событие")],
    ],
    resize_keyboard=True,
)



@dp.message(CommandStart())
async def start_my_bot(message : Message):
    await message.answer(f"""
🐾 Привет, {message.from_user.full_name}!

Я помогу заботиться о твоём питомце и помнить о важных делах 🐶🐱

🍽 Кормление
💊 Приём лекарств
💉 Прививки и посещения ветеринара

Давай познакомимся с твоим любимцем! Напиши /add_pet Барсик кот 👇
Или если нужна помощ то нажимай /help
""", reply_markup=main_kb)




@dp.message(Command("help"))
async def help_user(message : Message):
    try:
        await message.answer("""
🐾 Все команды и примеры:

/start — начать работу и показать кнопки
/help — показать эту подсказку
/add_pet Барсик кот — добавить питомца с именем Барсик и видом кот
/my_pets — показать своих питомцев и их ID
/log_care 3 feeding — записать уход (feeding / vet_visit / vaccination)
/feeding_pet id — записать кормление питомца №3
/vet_visit_pet id — записать визит питомца №3 к ветеринару
/vaccination_pet id — записать прививку питомца №3
/pet_history id — показать историю ухода за питомцем №3
/last_vaccination id — показать дату последней прививки питомца №3
/pets_needing_vaccination id — проверить необходимость прививки у питомца №3 (команда пока требует исправления)

""")
    except Exception as erorr:
        print("Help command erorr:", erorr)





@dp.message(Command("add_pet"))
async def create_new_pet(messaga : Message, command : CommandObject):
    try:
        example = command.args
        example = example.split("/")
        res = await create_pet(messaga.from_user.id ,example[0], example[1])
        if not res:
            await messaga.answer("Erorr add pet")
        else:
            await messaga.answer("Pet create sucessful 👌🏿")
    except:
        await messaga.answer("Напиши: /add_pet name/type")





@dp.message(F.text == "🐾 Мои питомцы")
@dp.message(Command("my_pets"))
async def print_my_pets(message : Message):
    try:
        petsy = await my_pets(message.from_user.id)
        result = ""
        if not petsy:
            print("У тя нету такого питомца")
        for i in petsy:
            result += f"""
    === Id {i['id']} ===
    Name: {i['name']} 
    Species: {i['species']} 
    """
        await message.answer(result)
    except:
        print("У тя нету питомев")








@dp.message(F.text == "📋 Добавить событие")
async def add_event_menu(message: Message):
    await message.answer("""
Запиши событие, например:
/log_care 3 feeding

Или выбери отдельную команду:

/feeding_pet id — покармит тамагочи
/vet_visit_pet id — ветеренар
/vaccination_pet id — прививка
""")





@dp.message(Command("feeding_pet"))
async def feeding_for_me(message : Message, command : CommandObject):
    try:
        example = command.args
        result = await log_care(message.from_user.id, int(example), 'feeding')
        await message.answer(result)   
    except:
        await message.answer("ОШИБКА !!! Пример: /feeding_pet id")

@dp.message(Command("vet_visit_pet"))
async def vet_visit_for_me(message : Message, command : CommandObject):
    try:
        example1 = command.args
        result = await log_care(message.from_user.id, int(example1), 'vet_visit')
        await message.answer(result)
    except:
        await message.answer("ты ошибся вот пример: /vet_visit_pet id")



@dp.message(Command("vaccination_pet"))
async def vaccination_for_me(message : Message, command : CommandObject):
    try:
        example2 = command.args
        result = await log_care(message.from_user.id, int(example2), 'vaccination')
        await message.answer(result)
    except:
            await message.answer("ты ошибся вот пример: /vaccination_pet id")








@dp.message(Command("log_care"))
async def add_care(message: Message, command: CommandObject):
    try:
        args = command.args.split("/")
        result = await log_care(message.from_user.id, int(args[0]), args[1])
        await message.answer(result)
    except Exception:
            await message.answer("ты ошибся вот пример: /log_care id")



@dp.message(Command("pet_history"))
async def his(messaga : Message ,command : CommandObject):
    try:    
        examle = command.args
        pet_id = int(examle)
        if not await pet_is_mine(messaga.from_user.id, pet_id):
            await messaga.answer("Питомец не найден")
            return
        pets = await my_history_vacanication(pet_id)
        if not pets:
            await messaga.answer("У этого питомца пока нет истории")
        resutation = ""
        for i in pets:
            resutation += f"""
    === Pet id {i['pet_id']} ===
    type: {i['type']} 
    logged_at: {i['logged_at']} 
    """
        await messaga.answer(resutation)
    except:
            await messaga.answer("ты ошибся вот пример: /pet_history id")





@dp.message(Command("pets_needing_vaccination"))
async def pets_needing_vaccination_now(messaga : Message ,command : CommandObject):
    try:
        examle = command.args
        a1 = await my_pet_need_vacanication(int(examle))
        if not a1:
            await messaga.answer("Not found")

        for i in a1:
            print(f"""
    type: {i['type']} 
    logged_at: {i['logged_at']} 
    """)
        await messaga.answer(a1)
    except:
        print("pets_needing_vaccination erorr")




@dp.message(Command("last_vaccination"))
async def last_vaccination(message: Message, command: CommandObject):
    try:
        pet = await get_last_vaccination(message.from_user.id, int(command.args))
        if not pet:
            await message.answer("Питомец не найден")
            return
        await message.answer(str(pet["last_vaccination"]))
    except Exception as erorr:
        await message.answer("Тут гдето ошибка нажми /help чтобы узнат правелный ввод")



async def main():
    await create_table()
    print("Create table succesifull")
    await dp.start_polling(bot)
    print("Bot started")
    
    
    
if __name__ == "__main__":
    asyncio.run(main())


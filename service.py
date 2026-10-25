from conection import *



async def create_pet(user_id ,name, species):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into pets (user_id, name, species) Values
        ($1, $2, $3) 
                     """, str(user_id), name, species)
        return True
    except Exception as Error:
        print(f"Create pet Error: {Error}")
    finally:
        await conn.close()
        

async def my_pets(user_id):
    try:
        conn = await connection_db()
        pets = await conn.fetch("""
SELECT * FROM pets
WHERE user_id = $1
""", str(user_id))
        return pets
    except Exception as erorr:
        print("Show my pets erorr:", erorr)
    finally:
        await conn.close()





async def pet_is_mine(user_id, pet_id):
    conn = await connection_db()
    try:
        pet = await conn.fetchrow("""
SELECT id FROM pets 
WHERE id = $1 AND user_id = $2
""", pet_id, str(user_id))
        return pet 
    finally:
        await conn.close()


async def log_care(user_id, pet_id, type):
    if type != "feeding" or type != "vet_visit" or type != "vaccination":
        print("Можно только: feeding, vet_visit, vaccination")
    if not await pet_is_mine(user_id, pet_id):
        return "Питомец не найден"
    conn = await connection_db()
    try:
        await conn.execute("""
INSERT INTO care_logs (pet_id, type) VALUES 
($1, $2)
""", pet_id, type)
        print("")
    finally:
        await conn.close()


async def get_last_vaccination(user_id, pet_id):
    conn = await connection_db()
    try:
        pet = await conn.fetchrow("""
SELECT name FROM pets WHERE id = $1 AND user_id = $2
""", pet_id, str(user_id))
        if not pet:
            return None
        return await conn.fetchrow("""
SELECT MAX(logged_at) FROM care_logs
WHERE pet_id = $1 AND type = 'vaccination'
""", pet_id)
    finally:
        await conn.close()


async def my_history_vacanication(pet_id):
    try:
        conn = await connection_db()
        petsa = await conn.fetch("""
SELECT * FROM care_logs
WHERE pet_id = $1
LIMIT 10
""", pet_id)
        return petsa
    except Exception as erorr:
        print("Show my pets erorr:", erorr)
    finally:
        await conn.close()







from datetime import *

a = datetime.now()





async def my_pet_need_vacanication(pet_id):
    try:
        conn = await connection_db()
        car1 = petsa = await conn.fetch("""
SELECT * FROM care_logs
WHERE logged_at < $1 - 365
WHERE pet_id = $2
""", a, str(pet_id))
        return car1
    except Exception as erorr:
        print("Show my pets erorr:", erorr)
    finally:
        await conn.close()





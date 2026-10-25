from conection import *



async def create_pet(user_id ,name, species):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into pets (user_id, name, species) Values
        ($1, $2, $3) 
                     """, str(user_id), name, species)
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





async def log_care(user_id, pet_id, type):    
    try:
        conn = await connection_db()
        if type == "feeding":
            await conn.execute("""
                INSERT INTO care_logs (pet_id, type) VALUES
                ($1, 'feeding')
            """, pet_id)
        elif type == "vet_visit":
            await conn.exectue("""
                INSERT INTO care_logs (pet_id, type) VALUES
                ($1, 'vet_visit)
            """, pet_id)
        elif type == "vaccination":
            await conn.exectue("""
                INSERT INTO care_logs (pet_id, type) VALUES
                ($1, 'vaccination')
            """, pet_id)
        else:
            print("Eror type: you heve only 3 type \n1)feeding\2)nvet_visit\n3)vaccination")
    except Exception as erorr:
        print("Log care error:", erorr)
    finally:
        await conn.close()

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
        




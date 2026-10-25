from dotenv import load_dotenv
import asyncpg
import os


load_dotenv()



paswprd_db = os.getenv("PASSWORD")






async def connection_db():
    try:
        conn = await asyncpg.connect(
            host="localhost",
            port=5432,
            user="postgres",
            database="iogramm",
            password=paswprd_db
        )
        return conn
    except Exception as Error:
        print(f"Connection Error: {Error}")




async def create_table():
    try:
        conn = await connection_db()
        await conn.execute("""
Create table if not exists pets(
id serial primary key,
user_id varchar(30),
name varchar(30),
species varchar(30),
is_active boolean default true,
created_at timestamp default now()
);
""")
        await conn.execute("""
Create table if not exists care_logs(
id serial primary key,
pet_id int references pets(id),
type varchar(30),
logged_at timestamp default now(),
is_active boolean default true,
created_at timestamp default now()
)
""")
    except Exception as erorr:
        print("Create erorr:", erorr)
    finally:
        await conn.close()




        
        
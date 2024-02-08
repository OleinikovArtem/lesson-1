import aiosqlite
from helpers.config_reader import config

DATABASE_PATH = config.database_path.get_secret_value()


async def create_readings_table(db):
    await db.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address_id INTEGER NOT NULL,
                reading_date TEXT NOT NULL,
                electricity_day REAL,
                electricity_night REAL,
                gas REAL,
                water REAL,
                FOREIGN KEY (address_id) REFERENCES addresses (id)
            );
        """)


async def add_reading(address_id: int, reading_date: str, electricity_day: float, electricity_night: float, gas: float, water: float):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO readings (address_id, reading_date, electricity_day, electricity_night, gas, water) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (address_id, reading_date, electricity_day, electricity_night, gas, water))
        await db.commit()


async def get_readings_for_address(address_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT reading_date, electricity_day, electricity_night, gas, water FROM readings WHERE address_id = ?",
            (address_id,)
        )
        return await cursor.fetchall()

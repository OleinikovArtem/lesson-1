import aiosqlite
from helpers.config_reader import config

DATABASE_PATH = config.database_path.get_secret_value()


async def create_address_table(db):
    await db.execute("""
        CREATE TABLE IF NOT EXISTS addresses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            address TEXT NOT NULL
        );
    """)


async def add_address(user_id: int, address: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT INTO addresses (user_id, address) VALUES (?, ?)", (user_id, address))
        await db.commit()


async def get_addresses(user_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT id, address FROM addresses WHERE user_id = ?",
            (user_id,)
        )
        return await cursor.fetchall()


async def get_address(user_id: int, address: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        query = """
                SELECT id, user_id, address
                FROM addresses
                WHERE user_id = ? AND address = ?
            """
        cursor = await db.execute(
            query,
            (user_id, address)
        )

        row = await cursor.fetchall()
        found_address = row[0]
        await cursor.close()

        if found_address:
            address_data = {
                "id": found_address[0],
                "user_id": found_address[1],
                "address": found_address[2],
            }
            return address_data
        else:
            return None

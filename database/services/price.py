import aiosqlite
from helpers.config_reader import config

DATABASE_PATH = config.database_path.get_secret_value()


async def create_price_table(db):
    await db.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_type TEXT NOT NULL,
            price REAL NOT NULL,
            effective_date TEXT NOT NULL
        );
    """)


async def add_price(service_type: str, price: float, effective_date: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT INTO prices (service_type, price, effective_date) VALUES (?, ?, ?)", (service_type, price, effective_date))
        await db.commit()


async def get_latest_price(service_type: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("SELECT price FROM prices WHERE service_type = ? ORDER BY effective_date DESC LIMIT 1", (service_type,))
        price = await cursor.fetchone()
        return price[0] if price else None


async def get_all_prices():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT service_type, price, effective_date FROM prices ORDER BY effective_date DESC"
        )
        return await cursor.fetchall()


async def get_prices_for_date(service_type: str, specific_date: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT price FROM prices WHERE service_type = ? AND effective_date <= ? ORDER BY effective_date DESC LIMIT 1",
            (service_type, specific_date)
        )
        price = await cursor.fetchone()
        return price[0] if price else None

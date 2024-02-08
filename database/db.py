import aiosqlite
from helpers.config_reader import config
from database.services import create_address_table, create_price_table, create_readings_table
DATABASE_PATH = config.database_path.get_secret_value()


async def create_tables():
    async with aiosqlite.connect(DATABASE_PATH) as db:

        await create_address_table(db)

        await create_price_table(db)

        await create_readings_table(db)

        await db.commit()

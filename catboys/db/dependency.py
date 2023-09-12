from catboys.db import async_session


async def get_db():
    async with async_session() as session:
        async with session.begin():
            yield session

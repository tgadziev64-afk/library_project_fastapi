from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///library.db")

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with async_session_factory() as session:
        yield session

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    f"sqlite+aiosqlite:///{os.path.join(BASE_DIR, 'instance', 'cvmatcher.db')}"
)

engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    os.makedirs(os.path.join(BASE_DIR, 'instance'), exist_ok=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
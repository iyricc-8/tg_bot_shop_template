import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from db.models import Base

load_dotenv()

# ============ ВЫБОР БАЗЫ ДАННЫХ ============
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()

# SQLite конфигурация (по умолчанию)
if DB_TYPE == "sqlite":
    DB_PATH = os.path.join(os.path.dirname(__file__), "../bot_shop.db")
    DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"
    
# MySQL конфигурация
elif DB_TYPE == "mysql":
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "shop_db")
    
    DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# PostgreSQL конфигурация
elif DB_TYPE == "postgresql":
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "shop_db")
    
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

else:
    raise ValueError(f"Неподдерживаемый тип БД: {DB_TYPE}")

# ============ СОЗДАТЬ ENGINE ============
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """Инициализирует базу данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """Получить сессию БД"""
    async with AsyncSessionLocal() as session:
        yield session

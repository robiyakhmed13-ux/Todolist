from sqlalchemy import ForeignKey, String, BigInteger, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncConnection, AsynAttrs, AsyncSession, create_async_engine, async_sessionmaker
from datetime import datetime

engine = create_async_engine(urls= "sqlite+aiosqlite:///example.db", echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)





class Base(AsynAttrs, DeclarativeBase):
    pass



class User(Base):
    __tablename__ = "users"


    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    tg_id = mapped_column(BigInteger, unique=True, nullable=False)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    user: Mapped[int] = mapped_column(ForeignKey("users.id"), ondelete="CASCADE", nullable=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()  

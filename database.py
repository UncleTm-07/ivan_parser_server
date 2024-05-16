from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

engine = create_async_engine(
    'sqlite+aiosqlite:///database.db'
)

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class WorkersTable(Model):
    __tablename__ = 'workers'
    id: Mapped[int] = mapped_column(primary_key=True)
    lastName: Mapped[str]
    name: Mapped[str]
    institutionName: Mapped[str]
    position: Mapped[str]
    academicRank: Mapped[str]
    isScholar: Mapped[bool]
    isOrcid: Mapped[str]
    orcid_id: Mapped[Optional[str]]
    isScopus: Mapped[bool]


class UsersTable(Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]


class WorkerDataTable(Model):
    __tablename__ = 'worker_data'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    journalTitle: Mapped[str]
    publicationDate: Mapped[str]
    source: Mapped[str]
    worker_id: Mapped[int]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)



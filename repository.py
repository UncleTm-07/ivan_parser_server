from database import new_session, WorkersTable, UsersTable
from schemas import NewWorker, Worker, AuthUser, Sources
from sqlalchemy import select, update, delete
from datetime import datetime


class WorkersRepository:
    @classmethod
    async def create_new_worker(cls, worker_data: NewWorker) -> Worker:
        async with new_session() as session:
            worker_dict = worker_data.model_dump()
            worker = WorkersTable(**worker_dict)
            session.add(worker)
            await session.flush()
            await session.commit()
            return worker

    @classmethod
    async def get_all_workers(cls) -> list[Worker]:
        async with new_session() as session:
            query = select(WorkersTable)
            result = await session.execute(query)
            worker_modules = result.scalars().all()
            return worker_modules

    @classmethod
    async def get_worker_by_id(cls, worker_id: int) -> Worker:
        async with new_session() as session:
            query = select(WorkersTable).where(WorkersTable.id == worker_id)
            result = await session.execute(query)
            worker_modules = result.scalars().all()
            return worker_modules

    @classmethod
    async def delete_worker_by_id(cls, worker_id: int):
        async with new_session() as session:
            query = delete(WorkersTable).where(WorkersTable.id == worker_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_worker_by_id(cls, worker_id: int, worker_data: Worker):
        async with new_session() as session:
            query = update(WorkersTable).values(lastName=worker_data.lastName,
                                                name=worker_data.name,
                                                institutionName=worker_data.institutionName,
                                                position=worker_data.position,
                                                academicRank=worker_data.academicRank,
                                                orcid_id=worker_data.orcid_id).filter_by(id=worker_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_worker_source_by_worker_id(cls, worker_id: int, sources: Sources):
        async with new_session() as session:
            query = update(WorkersTable).values(isScholar=sources.isScholar,
                                                isOrcid=sources.isOrcid,
                                                isScopus=sources.isScopus).filter_by(id=worker_id)
            await session.execute(query)
            await session.commit()


class UsersRepository:
    @classmethod
    async def get_user(cls, user_data: AuthUser):
        async with new_session() as session:
            username = user_data.username
            query = select(UsersTable).where(UsersTable.username == username)
            result = await session.execute(query)
            worker_modules = result.scalars().all()
            return worker_modules

    @classmethod
    async def create_user(cls, user_data: AuthUser):
        async with new_session() as session:
            user_dict = user_data.model_dump()
            user = UsersTable(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()
            return user

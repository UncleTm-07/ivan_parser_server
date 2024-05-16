from fastapi import APIRouter

from repository import WorkersRepository, UsersRepository
from schemas import Worker, NewWorker, AuthUser, OrcidName, Sources
from service import get_orcid_id_by_name, get_orcid_work, get_works_of_worker

worker_router = APIRouter(
    prefix="/workers",
    tags=["Workers"]
)

user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)

worker_data_router = APIRouter(
    prefix="/data",
    tags=["Data"]
)


@worker_router.get("")
async def get_all_workers():
    workers = await WorkersRepository.get_all_workers()
    worker_data = []
    for worker in workers:
        data = await get_works_of_worker(worker)
        worker.works = data
        worker_data.append(worker)
    return worker_data


@worker_router.get("/{worker_id}")
async def get_worker_by_id(worker_id: int):
    worker_module = await WorkersRepository.get_worker_by_id(worker_id)
    worker = worker_module[0]
    data = await get_works_of_worker(worker)
    worker.works = data
    return worker


@worker_router.post("")
async def create_worker(worker_data: NewWorker):
    orcid_id = await get_orcid_id_by_name(worker_data)
    if orcid_id:
        worker_data.orcid_id = orcid_id
        worker = await WorkersRepository.create_new_worker(worker_data)
        data = await get_works_of_worker(worker)
        worker.works = data
    else:
        worker = await WorkersRepository.create_new_worker(worker_data)
    return worker


@worker_router.delete("/{worker_id}")
async def delete_worker_by_id(worker_id: int):
    await WorkersRepository.delete_worker_by_id(worker_id)
    workers = await WorkersRepository.get_all_workers()
    worker_data = []
    for worker in workers:
        data = await get_works_of_worker(worker)
        worker.works = data
        worker_data.append(worker)
    return worker_data


@worker_router.put("/{worker_id}")
async def update_worker_by_id(worker_id: int, worker_data: Worker):
    await WorkersRepository.update_worker_by_id(worker_id, worker_data)
    workers = await WorkersRepository.get_all_workers()
    worker_data = []
    for worker in workers:
        data = await get_works_of_worker(worker)
        worker.works = data
        worker_data.append(worker)
    return worker_data


@worker_router.put("/source/{worker_id}")
async def update_worker_source_by_worker_id(worker_id: int, sources: Sources):
    print(sources)
    await WorkersRepository.update_worker_source_by_worker_id(worker_id, sources)
    workers = await WorkersRepository.get_all_workers()
    worker_data = []
    for worker in workers:
        data = await get_works_of_worker(worker)
        worker.works = data
        worker_data.append(worker)
    return worker_data


@worker_data_router.post("")
async def get_worker_data(data: OrcidName):
    orcid_id = await get_orcid_id_by_name(data)
    print(orcid_id)
    works = await get_orcid_work(orcid_id)
    print(works)
    return works


@user_router.post("/registration")
async def registration(user_data: AuthUser):
    result = await UsersRepository.get_user(user_data)
    if result:
        return {
            "message": "Користувач з таким usename вже існує!",
            "status": False
        }
    else:
        user = await UsersRepository.create_user(user_data)
        return {
            "username": user.username,
            "status": True
        }


@user_router.post("/login")
async def login(user_data: AuthUser):
    result = await UsersRepository.get_user(user_data)
    if result:
        user = result[0]  # Assuming the first element is the user
        print(user)
        if user.password == user_data.password:
            return {
                "message": "Пароль",
                "status": True
            }
        else:
            return {
                "message": "Не правильно вказаний пароль",
                "status": False
            }
    else:
        return {
            "message": "Користувач з таким usename не існує!",
            "status": False
        }

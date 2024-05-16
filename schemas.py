from typing import Optional

from pydantic import BaseModel, json
from sqlalchemy import TypeDecorator, Unicode


class NewWorker(BaseModel):
    lastName: str
    name: str
    institutionName: str
    position: str
    academicRank: str
    isScholar: bool
    isOrcid: bool
    orcid_id: Optional[str] = None
    isScopus: bool


class Worker(NewWorker):
    id: int


class Sources(BaseModel):
    isScholar: bool
    isOrcid: bool
    isScopus: bool


class AuthUser(BaseModel):
    username: str
    password: str


class OrcidName(BaseModel):
    lastName: str
    name: str
    institutionName: str


class JSONType(TypeDecorator):
    impl = Unicode

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

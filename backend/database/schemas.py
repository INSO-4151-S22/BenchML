from datetime import datetime
from typing import List, Literal, Set
from pydantic import BaseModel
from typing import Optional


class OrganizationBase(BaseModel):
    oid: int
    name: str
    owner_id: int
    owner: Optional['UserBaseRef']

    class Config:
        orm_mode = True


class Organization(OrganizationBase):
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    oid: Optional[int]

    class Config:
        orm_mode = True


class UserBaseRef(UserCreate):
    uid: int


class UserBase(UserBaseRef):
    organization: Optional[OrganizationBase]


class User(UserBase):
    created_at: datetime
    updated_at: datetime






class ModelBase(BaseModel):
    name: str
    source: str
    oid: Optional[int]


class ModelCreate(ModelBase):
    modules: Set[Literal["optimizer"]]


class Model(ModelBase):
    mid: int
    uploaded_at: datetime
    uid: int
    oid: Optional[int]
    user: UserBase
    organization: Optional[OrganizationBase]

    class Config:
        orm_mode = True


class ModelResultsCreate(BaseModel):
    information: str
    detail: str
    mid: int
    type: str

    class Config:
        orm_mode = True


class ModelResults(ModelResultsCreate):
    rid: int
    created_at: datetime
    model: Model


class ModelTaskCreate(BaseModel):
    tid: str
    mid: int
    type: str
    queue: str


class ModelTask(ModelTaskCreate):
    created_at: datetime

    class Config:
        orm_mode = True


class ModelStatus(BaseModel):
    mid: int
    type: str
    status: str
    created_at: datetime


OrganizationBase.update_forward_refs()
Organization.update_forward_refs()

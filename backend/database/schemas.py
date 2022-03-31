from datetime import datetime
from typing import List, Literal, Set
from pydantic import BaseModel


class UserBase(BaseModel):
    uid: int
    first_name: str
    last_name: str
    email: str
    rid: int
    oid: int

    class Config:
        orm_mode = True


class Role(BaseModel):
    rid: int
    type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Organization(BaseModel):
    oid: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class User(UserBase):
    uid: int
    created_at: datetime
    updated_at: datetime
    role: Role
    organization: Organization

    class Config:
        orm_mode = True


class ModelBase(BaseModel):
    name: str
    source: str


class ModelCreate(ModelBase):
    modules: Set[Literal["optimizer"]]


class Model(ModelBase):
    mid: int
    uploaded_at: datetime
    uid: int
    user: User

    class Config:
        orm_mode = True


class Category(BaseModel):
    cid: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class BenchmarkingDetailsCreate(BaseModel):
    information: str
    detail: str
    mid: int
    cid: int


class BenchmarkingDetails(BenchmarkingDetailsCreate):
    bdid: int
    created_at: datetime
    model: Model
    category: Category

    class Config:
        orm_mode = True


class OptimizationDetailsCreate(BaseModel):
    information: str
    detail: str
    mid: int
    cid: int


class OptimizationDetails(OptimizationDetailsCreate):
    odid: int
    created_at: datetime
    model: Model
    category: Category

    class Config:
        orm_mode = True


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


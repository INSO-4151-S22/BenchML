from typing import List, Optional
from datetime import datetime
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


class Model(BaseModel):
    mid: int
    name: str
    source: str
    uploaded_at: datetime

    class Config:
        orm_mode = True


class Category(BaseModel):
    cid: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class BenchmarkingDetails(BaseModel):
    bdid: int
    information: str
    detail: str
    created_at: datetime
    model: Model
    category: Category

    class Config:
        orm_mode = True


class OptimizationDetails(BaseModel):
    odid: int
    information: str
    detail: str
    created_at: datetime
    model: Model
    category: Category

    class Config:
        orm_mode = True

from datetime import datetime
from typing import List, Literal, Set
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional


class OrganizationCreate(BaseModel):
    name: str
    invitees: Set[EmailStr]

    class Config:
        orm_mode = True


class OrganizationBase(BaseModel):
    oid: int
    owner_id: int
    name: str
    owner: Optional['UserBase']
    organization_invitations: Optional[List['UserOrganization']]

    class Config:
        orm_mode = True


class Organization(OrganizationBase):
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class UserBase(UserCreate):
    uid: int


class User(UserBase):
    created_at: datetime
    updated_at: datetime


class ModelBase(BaseModel):
    name: str
    source: HttpUrl
    oid: Optional[int]
    type: Literal["pytorch", "keras"]


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


class UserOrganizationCreate(BaseModel):
    email: str
    oid: int

    class Config:
        orm_mode = True


class UserOrganization(UserOrganizationCreate):
    uoid: int
    accepted: bool
    created_at: datetime
    updated_at: datetime


OrganizationBase.update_forward_refs()
Organization.update_forward_refs()

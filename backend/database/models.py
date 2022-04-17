from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from config.database import Base
from sqlalchemy.types import LargeBinary


class Organization(Base):
    __tablename__ = "organization"

    oid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("users.uid"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    owner = relationship("User", back_populates="organization_managed",
                         primaryjoin="Organization.owner_id==User.uid")
    models = relationship("Model", back_populates="organization")
    organization_invitations = relationship("UserOrganizations", back_populates="organization",
                                            primaryjoin="UserOrganizations.oid==Organization.oid")


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    organization_managed = relationship(
        Organization, back_populates="owner", primaryjoin="Organization.owner_id==User.uid")
    model = relationship("Model", back_populates="user")


class Model(Base):
    __tablename__ = "model"

    mid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    source = Column(String)
    uploaded_at = Column(DateTime)
    uid = Column(Integer, ForeignKey("users.uid"))
    oid = Column(Integer, ForeignKey("organization.oid"))
    organization = relationship("Organization", back_populates="models")
    user = relationship("User", back_populates="model")
    model_results = relationship(
        "ModelResults", back_populates="model")
    model_task = relationship("ModelTask", back_populates="model")


class ModelResults(Base):
    __tablename__ = "model_results"

    rid = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    information = Column(String)
    detail = Column(String)
    created_at = Column(DateTime)
    mid = Column(Integer, ForeignKey("model.mid"))
    model = relationship("Model", back_populates="model_results")


class CeleryTaskMeta(Base):
    __tablename__ = "celery_taskmeta"

    task_id = Column(String, primary_key=True)
    status = Column(String)
    result = Column(LargeBinary)


class ModelTask(Base):
    __tablename__ = "model_task"

    tid = Column(String, primary_key=True, index=True)
    type = Column(String)
    queue = Column(String)
    created_at = Column(DateTime)
    mid = Column(Integer, ForeignKey("model.mid"))
    model = relationship("Model", back_populates="model_task")


class UserOrganizations(Base):
    __tablename__ = "user_organizations"

    uoid = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    accepted = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    oid = Column(Integer, ForeignKey("organization.oid"))
    organization = relationship("Organization", back_populates="organization_invitations",
                                primaryjoin="UserOrganizations.oid==Organization.oid")
 
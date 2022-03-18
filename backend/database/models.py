from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from backend.config.database import Base


class Role(Base):
    __tablename__ = "role"

    rid = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    users = relationship("User", back_populates="role")


class Organization(Base):
    __tablename__ = "organization"

    oid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    users = relationship("User", back_populates="organization")


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    rid = Column(Integer, ForeignKey("role.rid"))
    oid = Column(Integer, ForeignKey("organization.oid"))
    role = relationship("Role", back_populates="users")
    organization = relationship("Organization", back_populates="users")
    model = relationship("Model", back_populates="user")


class Model(Base):
    __tablename__ = "model"

    mid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    source = Column(String)
    uploaded_at = Column(DateTime)
    uid = Column(Integer, ForeignKey("users.uid"))
    user = relationship("User", back_populates="model")
    benchmarking_details = relationship("BenchmarkingDetails", back_populates="model")
    optimization_details = relationship("OptimizationDetails", back_populates="model")


class Category(Base):
    __tablename__ = "category"

    cid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    benchmarking_details = relationship("BenchmarkingDetails", back_populates="category")
    optimization_details = relationship("OptimizationDetails", back_populates="category")


class BenchmarkingDetails(Base):
    __tablename__ = "benchmarking_details"

    bdid = Column(Integer, primary_key=True, index=True)
    information = Column(String)
    detail = Column(String)
    created_at = Column(DateTime)
    mid = Column(Integer, ForeignKey("model.mid"))
    cid = Column(Integer, ForeignKey("category.cid"))
    model = relationship("Model", back_populates="benchmarking_details")
    category = relationship("Category", back_populates="benchmarking_details")


class OptimizationDetails(Base):
    __tablename__ = "optimization_details"

    odid = Column(Integer, primary_key=True, index=True)
    information = Column(String)
    detail = Column(String)
    created_at = Column(DateTime)
    mid = Column(Integer, ForeignKey("model.mid"))
    cid = Column(Integer, ForeignKey("category.cid"))
    model = relationship("Model", back_populates="optimization_details")
    category = relationship("Category", back_populates="optimization_details")

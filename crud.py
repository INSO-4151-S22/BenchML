from sqlalchemy.orm import Session
import models


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_roles(db: Session):
    return db.query(models.Role).all()


def get_organizations(db: Session):
    return db.query(models.Organization).all()


def get_models(db: Session):
    return db.query(models.Model).all()


def get_categories(db: Session):
    return db.query(models.Category).all()


def get_benchmarking_details(db: Session):
    return db.query(models.BenchmarkingDetails).all()


def get_optimization_details(db: Session):
    return db.query(models.OptimizationDetails).all()


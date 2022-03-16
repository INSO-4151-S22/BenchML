from sqlalchemy.orm import Session
from database import models, schemas
import pytz
from datetime import datetime


def get_datetime_now():
    pr = pytz.timezone('America/Puerto_Rico')
    return datetime.now(pr)


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


def get_model(db: Session, model_id: int):
    return db.query(models.Model).filter(models.Model.mid == model_id).first()


def create_model(db: Session, model: schemas.ModelCreate):
    # TODO: once auth is creates, uid should contain the actual user id
    current_datetime = get_datetime_now()
    db_model = models.Model(name=model.name, source=model.source,
                            uploaded_at=current_datetime, uid=1)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def get_categories(db: Session):
    return db.query(models.Category).all()


def get_benchmarking_details(db: Session):
    return db.query(models.BenchmarkingDetails).all()


def get_optimization_details(db: Session):
    return db.query(models.OptimizationDetails).all()

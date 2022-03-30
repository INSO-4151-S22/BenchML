from sqlalchemy.orm import Session
from backend.database import schemas, models
import pytz
from datetime import datetime
from backend.controller.tasks import optimize_model


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
    # TODO: implement categories
    # 1. create model
    current_datetime = get_datetime_now()
    db_model = models.Model(name=model.name, source=model.source,
                            uploaded_at=current_datetime, status="CREATED", uid=1)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)

    if 'optimizer' in model.modules:
        om = optimize_model.delay(model.source)
        model_task = schemas.ModelTaskCreate(tid=om.task_id, mid=db_model.mid, type="optimizer", queue="celery")
        create_model_task(db, model_task)
        # print('Call Optimizer')
        # try:
        #     res = Optimize().run(model.source)
        #     for r in res:
        #         optimization = schemas.OptimizationDetailsCreate(information=r.information, detail=r.detail,
        #                                                          mid=db_model.mid, cid=1)
        #         create_optimization_details(db, optimization)
        # except:
        #     optimization = schemas.OptimizationDetailsCreate(information='Error',
        #                                                      detail='There was an error optimizing your model. Please make sure to follow the guidelines.',
        #                                                      mid=db_model.mid, cid=1)
        #     create_optimization_details(db, optimization)
    return db_model


def get_categories(db: Session):
    return db.query(models.Category).all()


def get_benchmarking_details(db: Session):
    return db.query(models.BenchmarkingDetails).all()


def create_benchmarking_details(db: Session, model: schemas.BenchmarkingDetailsCreate):
    current_datetime = get_datetime_now()
    db_benchmarking_details = models.BenchmarkingDetails(information=model.information, detail=model.detail,
                                                         created_at=current_datetime, mid=model.mid, cid=model.cid)
    db.add(db_benchmarking_details)
    db.commit()
    db.refresh(db_benchmarking_details)
    return db_benchmarking_details


def get_optimization_details(db: Session):
    return db.query(models.OptimizationDetails).all()


def create_optimization_details(db: Session, model: schemas.OptimizationDetailsCreate):
    current_datetime = get_datetime_now()
    db_optimization_details = models.OptimizationDetails(information=model.information, detail=model.detail,
                                                         created_at=current_datetime, mid=model.mid, cid=model.cid)
    db.add(db_optimization_details)
    db.commit()
    db.refresh(db_optimization_details)
    return db_optimization_details


def get_celery_meta(db: Session):
    return db.query(models.CeleryTaskMeta).all()


def create_model_task(db: Session, model: schemas.ModelTaskCreate):
    current_datetime = get_datetime_now()
    db_model_task = models.ModelTask(tid=model.tid, mid=model.mid, type=model.type, queue=model.queue,
                                     created_at=current_datetime)
    db.add(db_model_task)
    db.commit()
    db.refresh(db_model_task)
    return db_model_task

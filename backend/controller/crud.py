from sqlalchemy.orm import Session
from backend.database import schemas, models
import pytz
from datetime import datetime
from backend.controller.tasks import optimize_model
from sqlalchemy import inspect
import pickle
import json


def get_datetime_now():
    pr = pytz.timezone('America/Puerto_Rico')
    return datetime.now(pr)


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()





def get_organizations(db: Session):
    return db.query(models.Organization).all()


def get_models(db: Session):
    return db.query(models.Model).all()


def get_model(db: Session, model_id: int):
    db_model = db.query(models.Model).filter(
        models.Model.mid == model_id).first()
    if db_model:
    verify_model_tasks(db, db_model)
    return db_model


def get_model_status_by_model_id(db: Session, model_id: int):
    db_model = get_model(db, model_id)
    if not db_model:
        return db_model

    db_model_status = db.query(models.ModelTask.mid, models.ModelTask.type, models.ModelTask.created_at, models.CeleryTaskMeta.status).filter(
        models.ModelTask.tid == models.CeleryTaskMeta.task_id).filter(models.ModelTask.mid == model_id).all()

    return db_model_status


def create_model(db: Session, model: schemas.ModelCreate):
    # TODO: once auth is creates, uid should contain the actual user id
    # 1. create model
    current_datetime = get_datetime_now()
    db_model = models.Model(name=model.name, source=model.source,
                            uploaded_at=current_datetime, uid=1)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)

    if 'optimizer' in model.modules:
        om = optimize_model.delay(model.source)
        model_task = schemas.ModelTaskCreate(
            tid=om.task_id, mid=db_model.mid, type="optimizer", queue="celery")
        create_model_task(db, model_task)
    return db_model


def get_model_results_by_model_id(db: Session, model_id: int, **kwargs):
    if 'type' in kwargs:
        return db.query(models.ModelResults).filter(models.ModelResults.mid == model_id).filter(models.ModelResults.type == kwargs.get('type')).all()

    return db.query(models.ModelResults).filter(models.ModelResults.mid == model_id).all()


def create_model_results(db: Session, model: schemas.ModelResultsCreate):
    current_datetime = get_datetime_now()
    db_model_results = models.ModelResults(information=model.information, detail=model.detail,
                                           created_at=current_datetime, mid=model.mid, type=model.type)
    db.add(db_model_results)
    db.commit()
    db.refresh(db_model_results)
    return db_model_results


def get_celery_taskmeta_by_task_id(db: Session, celery_taskmeta_task_id: int):
    return db.query(models.CeleryTaskMeta).filter(models.CeleryTaskMeta.task_id == celery_taskmeta_task_id).first()


def get_celery_taskmetas(db: Session):
    return db.query(models.CeleryTaskMeta).all()


def get_model_tasks_by_model_id(db: Session, model_id: int, type=None):
    if type in ['optimizer']:
        return db.query(models.ModelTask).filter(models.ModelTask.mid == model_id, models.ModelTask.type == type).first()
    else:
        return db.query(models.ModelTask).filter(models.ModelTask.mid == model_id).all()


def create_model_task(db: Session, model: schemas.ModelTaskCreate):
    current_datetime = get_datetime_now()
    db_model_task = models.ModelTask(tid=model.tid, mid=model.mid, type=model.type, queue=model.queue,
                                     created_at=current_datetime)
    db.add(db_model_task)
    db.commit()
    db.refresh(db_model_task)
    return db_model_task


#
# -- Helper Funcions --
#
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


# Check if the celery task has finished or failed and fetch that data (if not done previously)
def verify_model_tasks(db: Session, model: schemas.Model):
    # Optimization
    od = get_model_results_by_model_id(db, model.mid, type='optimizer')
    if not od:
        model_tasks = get_model_tasks_by_model_id(db, model.mid, 'optimizer')
        taskmeta = get_celery_taskmeta_by_task_id(db, model_tasks.tid)

        if taskmeta.status == 'FAILURE':
            optimization = schemas.ModelResultsCreate(
                type='optimizer', information='Error', detail='There was an error optimizing your model. Please make sure to follow the guidelines.', mid=model.mid)
            create_model_results(db, optimization)

        elif taskmeta.status == 'SUCCESS':
            data = object_as_dict(taskmeta)
            res = pickle.loads(data['result'])
            for k in res:
                optimization = schemas.ModelResultsCreate(type='optimizer', information=str(k), detail=json.dumps(res[k]),
                                                          mid=model.mid)
                create_model_results(db, optimization)

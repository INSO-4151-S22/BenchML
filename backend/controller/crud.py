from sqlalchemy.orm import Session
from database import schemas, models
import pytz
from datetime import datetime
from controller.tasks import optimize_model
from sqlalchemy import inspect
import pickle
import json


def get_datetime_now():
    pr = pytz.timezone('America/Puerto_Rico')
    return datetime.now(pr)


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, model: schemas.UserCreate):
    current_datetime = get_datetime_now()
    db_user = models.User(first_name=model.first_name, last_name=model.last_name,
                          updated_at=current_datetime, created_at=current_datetime, email=model.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def __create_user_organizations(db: Session, model: schemas.UserOrganizationCreate, owner: bool = False):
    current_datetime = get_datetime_now()
    db_invitation = models.UserOrganizations(
        email=model.email, oid=model.oid, updated_at=current_datetime, created_at=current_datetime, accepted=owner)
    db.add(db_invitation)
    db.commit()
    db.refresh(db_invitation)
    return db_invitation


def get_organizations(db: Session, user: schemas.User):
    return db.query(models.Organization, models.UserOrganizations).filter(models.UserOrganizations.oid == models.Organization.oid).filter(
        models.UserOrganizations.email == user.email).filter(models.UserOrganizations.accepted == True).with_entities(models.Organization).all()


def get_organizations_by_id(db: Session, organization_id: int, user: schemas.User):
    return db.query(models.Organization, models.UserOrganizations).filter(models.UserOrganizations.oid == models.Organization.oid).filter(models.UserOrganizations.email == user.email).filter(models.UserOrganizations.accepted == True).with_entities(models.Organization).filter(models.Organization.oid == organization_id).first()


def get_user_organizations(db: Session, user: schemas.User):
    return db.query(models.UserOrganizations).join(models.User, models.UserOrganizations.email == models.User.email).filter(models.User.uid == user.uid).all()


def get_user_organizations_by_id(db: Session, user: schemas.User, invitation_id: int):
    return db.query(models.UserOrganizations).join(models.User, models.UserOrganizations.email == models.User.email).filter(models.User.uid == user.uid).filter(models.UserOrganizations.uoid == invitation_id).first()


def set_user_organizations_accept(db: Session, user: schemas.User, invitation_id: int):
    invitation = get_user_organizations_by_id(db, user, invitation_id)

    if not invitation or invitation.accepted:
        return invitation

    current_datetime = get_datetime_now()
    invitation.accepted = True
    invitation.updated_at = current_datetime
    db.commit()
    db.refresh(invitation)
    return invitation


def create_organization(db: Session, model: schemas.OrganizationCreate, user: schemas.User):
    current_datetime = get_datetime_now()
    db_organization = models.Organization(name=model.name, owner_id=user.uid,
                                          updated_at=current_datetime, created_at=current_datetime)
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)

    db_user_organization = schemas.UserOrganizationCreate(
        email=user.email, oid=db_organization.oid)
    __create_user_organizations(db, db_user_organization, True)

    for invited in model.invitees:
        i = schemas.UserOrganizationCreate(
            email=invited, oid=db_organization.oid)
        __create_user_organizations(db, i)

    return db_organization


def get_models(db: Session, user: schemas.User):
    m_organizations = db.query(models.UserOrganizations).filter(models.UserOrganizations.email == user.email).filter(
        models.UserOrganizations.accepted == True).join(models.Model, models.Model.oid == models.UserOrganizations.oid).with_entities(models.Model)
    m = db.query(models.Model).join(models.User, models.User.email == user.email).filter(
        models.Model.oid.is_(None)).with_entities(models.Model)
    return m.union(m_organizations).all()


def get_model(db: Session, model_id: int, user: schemas.User):
    db_model = db.query(models.Model).join(models.User, models.Model.uid == models.User.uid).filter(models.User.uid == user.uid).filter(
        models.Model.mid == model_id).first()
    if db_model:
        __verify_model_tasks(db, db_model, user)
    return db_model


def get_model_status_by_model_id(db: Session, model_id: int, user: schemas.User):
    db_model = get_model(db, model_id, user)
    if not db_model:
        return db_model

    db_model_status = db.query(models.ModelTask.mid, models.ModelTask.type, models.ModelTask.created_at, models.CeleryTaskMeta.status).filter(
        models.ModelTask.tid == models.CeleryTaskMeta.task_id).filter(models.User.uid == user.uid).filter(models.ModelTask.mid == model_id).all()

    return db_model_status


def create_model(db: Session, model: schemas.ModelCreate, user: schemas.User):
    # TODO: once auth is creates, uid should contain the actual user id
    # 1. create model
    current_datetime = get_datetime_now()
    db_model = models.Model(name=model.name, source=model.source, oid=model.oid,
                            uploaded_at=current_datetime, uid=user.uid)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)

    if 'optimizer' in model.modules:
        om = optimize_model.delay(model.source)
        model_task = schemas.ModelTaskCreate(
            tid=om.task_id, mid=db_model.mid, type="optimizer", queue="celery")
        __create_model_task(db, model_task, user)
    return db_model


def get_model_results_by_model_id(db: Session, model_id: int, user: schemas.User, **kwargs):
    if 'type' in kwargs:
        return db.query(models.ModelResults).join(models.Model, models.ModelResults.mid == models.Model.mid).join(models.User, models.Model.uid == models.User.uid).filter(models.User.uid == user.uid).filter(models.ModelResults.mid == model_id).filter(models.ModelResults.type == kwargs.get('type')).all()

    return db.query(models.ModelResults).join(models.Model, models.ModelResults.mid == models.Model.mid).join(models.User, models.Model.uid == models.User.uid).filter(models.User.uid == user.uid).filter(models.ModelResults.mid == model_id).all()


def __create_model_results(db: Session, model: schemas.ModelResultsCreate, user: schemas.User):
    current_datetime = get_datetime_now()
    db_model_results = models.ModelResults(information=model.information, detail=model.detail,
                                           created_at=current_datetime, mid=model.mid, type=model.type)
    db.add(db_model_results)
    db.commit()
    db.refresh(db_model_results)
    return db_model_results


def __get_celery_taskmeta_by_task_id(db: Session, celery_taskmeta_task_id: int, user: schemas.User):
    return db.query(models.CeleryTaskMeta).filter(models.CeleryTaskMeta.task_id == celery_taskmeta_task_id).first()


def __get_model_tasks_by_model_id(db: Session, model_id: int, user: schemas.User, type=None):
    if type in ['optimizer']:
        return db.query(models.ModelTask).filter(models.ModelTask.mid == model_id, models.ModelTask.type == type).first()
    else:
        return db.query(models.ModelTask).filter(models.ModelTask.mid == model_id).all()


def __create_model_task(db: Session, model: schemas.ModelTaskCreate, user: schemas.User):
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
def __object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


# Check if the celery task has finished or failed and fetch that data (if not done previously)
def __verify_model_tasks(db: Session, model: schemas.Model, user: schemas.User):
    # Optimization
    od = get_model_results_by_model_id(db, model.mid, user, type='optimizer')
    if not od:
        model_tasks = __get_model_tasks_by_model_id(
            db, model.mid, user, 'optimizer')
        taskmeta = __get_celery_taskmeta_by_task_id(db, model_tasks.tid, user)

        if taskmeta.status == 'FAILURE':
            optimization = schemas.ModelResultsCreate(
                type='optimizer', information='Error', detail='There was an error optimizing your model. Please make sure to follow the guidelines.', mid=model.mid)
            __create_model_results(db, optimization, user)

        elif taskmeta.status == 'SUCCESS':
            data = __object_as_dict(taskmeta)
            res = pickle.loads(data['result'])
            for k in res:
                optimization = schemas.ModelResultsCreate(type='optimizer', information=str(k), detail=json.dumps(res[k]),
                                                          mid=model.mid)
                __create_model_results(db, optimization, user)

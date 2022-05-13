from sqlalchemy.orm import Session
from database import schemas, models
import pytz
from datetime import datetime
from controller.tasks import optimize_model, adversarial_attack_model
from sqlalchemy import inspect
import pickle
import json
import config


def get_datetime_now():
    t_zone = pytz.timezone(config.get_settings().timezone)
    return datetime.now(t_zone)


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


def __create_user_organizations(db: Session, user_organization: schemas.UserOrganizationCreate, owner: bool = False):
    current_datetime = get_datetime_now()
    db_user_organization = models.UserOrganizations(
        email=user_organization.email, oid=user_organization.oid, updated_at=current_datetime, created_at=current_datetime, accepted=owner)
    db.add(db_user_organization)
    db.commit()
    db.refresh(db_user_organization)
    return db_user_organization


def get_organizations(db: Session, user: schemas.User):
    return db.query(models.Organization).join(models.UserOrganizations, models.UserOrganizations.oid == models.Organization.oid).filter(models.UserOrganizations.email == user.email).filter(models.UserOrganizations.accepted == True).with_entities(models.Organization).all()


def get_organizations_by_id(db: Session, organization_id: int, user: schemas.User):
    return db.query(models.Organization).join(models.UserOrganizations, models.UserOrganizations.oid == models.Organization.oid).filter(models.UserOrganizations.email == user.email).filter(models.UserOrganizations.accepted == True).filter(models.Organization.oid == organization_id).with_entities(models.Organization).first()


def get_user_organizations(db: Session, user: schemas.User):
    return db.query(models.UserOrganizations).filter(models.UserOrganizations.email == user.email).all()


def get_user_organizations_by_id(db: Session, user: schemas.User, invitation_id: int):
    return db.query(models.UserOrganizations).filter(models.UserOrganizations.email == user.email).filter(models.UserOrganizations.uoid == invitation_id).first()


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


def create_organization(db: Session, organization: schemas.OrganizationCreate, user: schemas.User):
    current_datetime = get_datetime_now()
    db_organization = models.Organization(name=organization.name, owner_id=user.uid,
                                          updated_at=current_datetime, created_at=current_datetime)
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)

    # create entry for owner
    db_user_organization = schemas.UserOrganizationCreate(
        email=user.email, oid=db_organization.oid)
    __create_user_organizations(db, db_user_organization, True)

    # create entry for invitees
    for invited in organization.invitees:
        # avoid owner added twice
        if invited == user.email:
            continue
        i = schemas.UserOrganizationCreate(
            email=invited, oid=db_organization.oid)
        __create_user_organizations(db, i)

    return db_organization


def __get_user_models(db: Session, user: schemas.User):
    m_organizations = db.query(models.UserOrganizations).filter(models.UserOrganizations.email == user.email).filter(
        models.UserOrganizations.accepted == True).join(models.Model, models.Model.oid == models.UserOrganizations.oid).with_entities(models.Model)
    m = db.query(models.Model).join(models.User, models.User.uid == models.Model.uid).filter(models.User.email == user.email).filter(
        models.Model.oid.is_(None)).with_entities(models.Model)
    return m.union(m_organizations)


def get_models(db: Session, user: schemas.User):
    return __get_user_models(db, user).all()


def get_model(db: Session, model_id: int, user: schemas.User):
    db_model = __get_user_models(db, user).filter(
        models.Model.mid == model_id).first()
    if db_model:
        __verify_model_tasks(db, db_model.mid, user)
    return db_model


def get_model_status_by_model_id(db: Session, model_id: int, user: schemas.User):
    # this will make sure that the user has permission to view that model
    db_model = get_model(db, model_id, user)
    if not db_model:
        return db_model

    db_model_status = db.query(models.ModelTask).join(
        models.CeleryTaskMeta, models.ModelTask.tid == models.CeleryTaskMeta.task_id).filter(models.ModelTask.mid == model_id).with_entities(models.ModelTask.mid, models.ModelTask.type, models.ModelTask.created_at, models.CeleryTaskMeta.status).all()

    return db_model_status


def create_model(db: Session, model: schemas.ModelCreate, user: schemas.User):
    current_datetime = get_datetime_now()
    db_model = models.Model(name=model.name, source=model.source, oid=model.oid,
                            uploaded_at=current_datetime, uid=user.uid, type=model.type)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)

    if 'optimizer' in model.modules:
        om = optimize_model.delay(model.source, model.type)
        model_task = schemas.ModelTaskCreate(
            tid=om.task_id, mid=db_model.mid, type="optimizer", queue="celery")
        __create_model_task(db, model_task, user)

    if 'adversarial' in model.modules:
        aam = adversarial_attack_model.delay(model.source, model.type)
        model_task = schemas.ModelTaskCreate(
            tid=aam.task_id, mid=db_model.mid, type="adversarial", queue="celery")
        __create_model_task(db, model_task, user)

    return db_model


def get_model_results_by_model_id(db: Session, model_id: int, user: schemas.User, **kwargs):
    db_models = __get_user_models(db, user).filter(
        models.Model.mid == model_id)

    # if called internally, avoid infinite loop
    if ('mode' not in kwargs or not kwargs.get('mode') == 'internal') and db_models.first():
        __verify_model_tasks(db, model_id, user)

    qry = db_models.join(models.ModelResults, models.ModelResults.mid ==
                         models.Model.mid).with_entities(models.ModelResults)
    if 'type' in kwargs:
        qry = qry.filter(models.ModelResults.type == kwargs.get('type'))

    return qry.all()


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
    if type in ['optimizer', 'adversarial']:
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


def __extract_model_task(db: Session, model_id: int, user: schemas.User, task_id: int, module_evaluation: str):
    taskmeta = __get_celery_taskmeta_by_task_id(db, task_id, user)
    # Store model results if has not started due to error or has finished with failure or success
    if not taskmeta:
        # This will get called in the case of Celery being down. Return in order to allow for later processing.
        return
    elif taskmeta.status == 'FAILURE':
        model_results = schemas.ModelResultsCreate(
            type=module_evaluation, information='Error', detail=f"There was an error performing {module_evaluation} module on your model. Please make sure to follow the guidelines.", mid=model_id)
        __create_model_results(db, model_results, user)

    elif taskmeta.status == 'SUCCESS':
        data = __object_as_dict(taskmeta)
        try:
            res = pickle.loads(data['result'])
            for k in res:
                model_results = schemas.ModelResultsCreate(type=module_evaluation, information=str(k), detail=json.dumps(res[k]), mid=model_id)
                __create_model_results(db, model_results, user)
        except Exception as e:
            return None


#
# -- Helper Funcions --
#
def __object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


# Check if the celery task has finished or failed and fetch that data (if not done previously)
def __verify_model_tasks(db: Session, model_id: int, user: schemas.User):
    # verify if results were already generated, meaning that this function was already called for this model
    od = get_model_results_by_model_id(db, model_id, user, type='optimizer', mode="internal")
    adv = get_model_results_by_model_id(db, model_id, user, type='adversarial', mode="internal")

    # if it was not executed prev, get the tasks created for the model
    od_model_tasks = __get_model_tasks_by_model_id(db, model_id, user, 'optimizer') if not od else None   
    adv_model_tasks = __get_model_tasks_by_model_id(db, model_id, user, 'adversarial') if not adv else None

    # use the tasks obtained to extract the data from celery's tables
    if(od_model_tasks):
        __extract_model_task(db, model_id, user, od_model_tasks.tid, 'optimizer')
    if(adv_model_tasks):
        __extract_model_task(db, model_id, user, adv_model_tasks.tid, 'adversarial')

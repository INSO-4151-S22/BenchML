from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from controller import crud, auth
from database import schemas, models
from config.database import SessionLocal
import config


app = FastAPI()
token_auth_scheme = HTTPBearer()


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get_settings().cors_allow_origins.split(','),
    allow_credentials=config.get_settings().cors_allow_credentials,
    allow_methods=config.get_settings().cors_allow_methods.split(','),
    allow_headers=config.get_settings().cors_allow_headers.split(','),
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def __record_not_found(model: str, id: int):
    raise HTTPException(
                status_code=404, detail=f"{model} item with id {id} not found")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(token_auth_scheme)):
    user = auth.VerifyToken(db, token.credentials).verify()

    if not type(user) == models.User:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.get("/organizations/", response_model=List[schemas.Organization])
def read_organizations(db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    organizations = crud.get_organizations(db, user)
    return organizations


@app.get("/organizations/invitations/", response_model=List[schemas.UserOrganization])
def read_organizations_invitations(db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    invitations = crud.get_user_organizations(db, user)
    return invitations


@app.post("/organizations/invitations/{invitation_id}/accept", response_model=schemas.UserOrganization)
def update_organizations_invitations_status(invitation_id: int, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    invitation = crud.set_user_organizations_accept(db, user, invitation_id)
    if not invitation:
        __record_not_found("Organization Invitation", invitation_id)
    return invitation


@app.post("/organizations/", response_model=schemas.Organization)
def create_organization(organization: schemas.OrganizationCreate, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    organization_insert = crud.create_organization(db, organization, user)
    return organization_insert


@app.get("/models/", response_model=List[schemas.Model])
def read_models(db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    models = crud.get_models(db, user)
    return models


@app.get("/models/{model_id}", response_model=schemas.Model)
async def read_model(model_id: int, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    model = crud.get_model(db, model_id, user)
    if not model:
        __record_not_found("Model", model_id)
    return model


@app.post("/models/", response_model=schemas.Model)
def create_model(model: schemas.ModelCreate, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    if model.oid == 0:
        __record_not_found("Organization", model.oid)
    elif model.oid:
        organization = crud.get_organizations_by_id(db, model.oid, user)
        if not organization:
            __record_not_found("Organization", model.oid)
    model_insert = crud.create_model(db, model, user)
    return model_insert


@app.get("/models/{model_id}/status/", response_model=List[schemas.ModelStatus])
async def read_model_status(model_id: int, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    model_status = crud.get_model_status_by_model_id(db, model_id, user)
    if not model_status:
        __record_not_found("Model Status for Model", model_id)
    return model_status


@app.get("/models/{model_id}/details/", response_model=List[schemas.ModelResults])
async def read_model_details(model_id: int, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    model_details = crud.get_model_results_by_model_id(db, model_id, user)
    if not model_details:
        __record_not_found("Model Results for Model", model_id)
    return model_details

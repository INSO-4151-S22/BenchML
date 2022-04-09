from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from controller import crud
from database import schemas
from config.database import SessionLocal


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Welcome to BenchML"}


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/organizations/", response_model=List[schemas.Organization])
def read_organizations(db: Session = Depends(get_db)):
    organizations = crud.get_organizations(db)
    return organizations


@app.get("/models/", response_model=List[schemas.Model])
def read_models(db: Session = Depends(get_db)):
    models = crud.get_models(db)
    return models


@app.get("/models/{model_id}", response_model=schemas.Model)
async def read_model(model_id: int, db: Session = Depends(get_db)):
    model = crud.get_model(db, model_id)
    if not model:
        raise HTTPException(
            status_code=404, detail=f"Model item with id {model_id} not found")
    return model


@app.post("/models/", response_model=schemas.Model)
def create_model(model: schemas.ModelCreate, db: Session = Depends(get_db)):
    model_insert = crud.create_model(db, model)
    return model_insert


@app.get("/models/{model_id}/status/", response_model=List[schemas.ModelStatus])
async def read_model_status(model_id: int, db: Session = Depends(get_db)):
    model_status = crud.get_model_status_by_model_id(db, model_id)
    if not model_status:
        raise HTTPException(
            status_code=404, detail=f"No Model Status for Model item with id {model_id} not found")
    return model_status


@app.get("/models/{model_id}/details/", response_model=List[schemas.ModelResults])
async def read_model_details(model_id: int, db: Session = Depends(get_db)):
    model_details = crud.get_model_results_by_model_id(db, model_id)
    if not model_details:
        raise HTTPException(
            status_code=404, detail=f"Model Results for Model item with id {model_id} not found")
    return model_details

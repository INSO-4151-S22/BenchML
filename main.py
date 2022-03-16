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


@app.get("/roles/", response_model=List[schemas.Role])
def read_roles(db: Session = Depends(get_db)):
    roles = crud.get_roles(db)
    return roles


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
        raise HTTPException(status_code=404, detail=f"Model item with id {model_id} not found")
    return model


@app.post("/models/", response_model=schemas.Model)
def create_model(model: schemas.ModelCreate, db: Session = Depends(get_db)):
    model_insert = crud.create_model(db, model)
    return model_insert


@app.get("/categories/", response_model=List[schemas.Category])
def read_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return categories


@app.get("/benchmarking_details/", response_model=List[schemas.BenchmarkingDetails])
def read_benchmarking_details(db: Session = Depends(get_db)):
    benchmarking_details = crud.get_benchmarking_details(db)
    return benchmarking_details


@app.get("/optimization_details/", response_model=List[schemas.OptimizationDetails])
def read_optimization_details(db: Session = Depends(get_db)):
    optimization_details = crud.get_optimization_details(db)
    return optimization_details

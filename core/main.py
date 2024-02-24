from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/{id}/", response_model=schemas.UserSchema, 
         response_model_exclude={'role'}, response_model_by_alias=False)
def get_user(id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with user id ({id}) not found")
    return db_user


@app.get("/users/email/{email}/", response_model=schemas.UserSchema, 
         response_model_exclude={'role'}, response_model_by_alias=False)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with email ({email}) not found")
    return db_user


@app.get("/users/", response_model=list[schemas.UserSchema], 
         response_model_exclude={'role'}, response_model_by_alias=False)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.post("/users/", response_model=schemas.UserSchema)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail=f"User with email `{user.email}` already registered")
    return crud.create_user(db=db, user=user)


# @app.post("/users/{id}/", response_model=schemas.UserSchema)
# def update_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, id=id)
#     if not db_user:
#         raise HTTPException(status_code=400, detail=f"User with user id ({id}) not found")
#     return crud.update_user(db=db, user=user)


@app.put("/users/{id}/", response_model=schemas.UserSchema)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    # TODO
    db_user = crud.get_user(db, id=id)
    if not db_user:
        raise HTTPException(status_code=400, detail=f"User with user id ({id}) not found")
    
    print(db_user)
    print(type(db_user))
    print('---------')
    
    print(user)
    print(type(user))
    
    return crud.update_user(db=db, user=user)


# ==================================Films URLs===================================

@app.get("/films/{id}/", response_model=schemas.FilmSchema, 
         response_model_exclude={'role'}, response_model_by_alias=False)
def get_film(id: int, db: Session = Depends(get_db)):
    db_film = crud.get_film(db, id=id)
    if db_film is None:
        raise HTTPException(status_code=404, detail=f"Film with film id ({id}) not found")
    return db_film


@app.get("/films/", response_model=list[schemas.FilmSchema], 
         response_model_exclude={'role'}, response_model_by_alias=False)
def get_films(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_films(db, skip=skip, limit=limit)


@app.post("/films/", response_model=schemas.Film, 
         response_model_exclude={'role'}, response_model_by_alias=False)
def create_film(film: schemas.FilmCreate, db: Session = Depends(get_db)):
    # TODO
    db_film = crud.create_film(db, email=film.email)
    if db_film:
        raise HTTPException(status_code=400, detail=f"Film with email `{film.email}` already registered")
    return crud.create_film(db=db, film=film)

# ==================================Company URLs===================================

@app.get("/companies/{id}/", response_model=schemas.CompanySchema, 
         response_model_exclude={'role'}, response_model_by_alias=False)
def get_company(id: int, db: Session = Depends(get_db)):
    db_company = crud.get_company(db, id=id)
    if db_company is None:
        raise HTTPException(status_code=404, detail=f"Company with company id ({id}) not found")
    return db_company


@app.get("/companies/", response_model=list[schemas.CompanySchema], 
         response_model_exclude={'role'}, response_model_by_alias=False)
def get_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_companies(db, skip=skip, limit=limit)


@app.post("/companies/", response_model=schemas.CompanyCreate, 
         response_model_exclude={'role'}, response_model_by_alias=False)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    # TODO
    db_company = crud.create_company(db, email=company.email)
    if db_company:
        raise HTTPException(status_code=400, detail=f"Company with email `{company.email}` already registered")
    return crud.create_company(db=db, company=company)


@app.put("/companies/{id}/", response_model=schemas.CompanyUpdate, 
         response_model_exclude={'role'}, response_model_by_alias=False)
def update_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    # TODO
    db_company = crud.update_company(db, email=company.email)
    if db_company:
        raise HTTPException(status_code=400, detail=f"Company with email `{company.email}` already registered")
    return crud.create_company(db=db, company=company)

# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session, load_only

import typing
from core.models import Company
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


@app.post("/users/", response_model=schemas.UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreateSchema, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail=f"User with email `{user.email}` already registered")
    return crud.create_user(db=db, user=user)


@app.post("/users/{id}/", response_model=schemas.UserSchema)
def update_user(id: int, user: schemas.UserUpdateSchema, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, id=id)
    if not db_user:
        raise HTTPException(status_code=400, detail=f"User with user id ({id}) not found")
    
    if user.id != id:
        # To ensure consistency between the accessed and updated instance
        raise HTTPException(status_code=400, detail=f"Suspicious operation identified User bject")
    
    fids = list(map(lambda x: x.get('film', {}).get('id', None), user.dict().get('films', [])))
    existing_fids = list(map(lambda x: x.film.id, db_user.films))
    
    if len(fids) > 0:
        # db_fids = list(map(lambda x: x[0], db.query(models.Film.id).filter(models.Film.id.in_(fids)).all()))
        for fid in fids:
            if fid and not fid in existing_fids:
                print("****This is wrong either by error or malnipulative attempt? ", fid)
                raise HTTPException(status_code=400, detail=f"Suspicious operation identified with the list of Films")
        
    cids = list(map(lambda x: x.get('company', {}).get('id', None), user.dict().get('companies', [])))
    existing_cids = list(map(lambda x: x.company.id, db_user.companies))
    
    if len(cids) > 0:
        for cid in cids:
            if cid and not cid in existing_cids:
                print("****This is wrong either by error or malnipulative attempt? ", cid)
                raise HTTPException(status_code=400, detail=f"Suspicious operation identified with the list of Companies")
        
    return crud.update_user_post(db=db, user=user)


# @app.put("/users/{id}/", response_model=schemas.UserSchema)
# def update_user(id: int, user: schemas.UserUpdateSchema, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, id=id)
#     if not db_user:
#         raise HTTPException(status_code=400, detail=f"User with user id ({id}) not found")
#     if user.id != id:
#         # To ensure consistency between the accessed and updated instance
#         raise HTTPException(status_code=400, detail=f"Suspicious operation identified")
#     return crud.update_user_put(db=db, user=user)


# ==================================Films URLs===================================

@app.get("/films/{id}/", response_model=schemas.FilmSchema)
def get_film(id: int, db: Session = Depends(get_db)):
    db_film = crud.get_film(db, id=id)
    if db_film is None:
        raise HTTPException(status_code=404, detail=f"Film with film id ({id}) not found")
    return db_film


@app.get("/films/", response_model=list[schemas.FilmSchema])
def get_films(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_films(db, skip=skip, limit=limit)


@app.post("/films/", response_model=schemas.FilmSchema, status_code=status.HTTP_201_CREATED)
def create_film(film: schemas.FilmCreateSchema, db: Session = Depends(get_db)):
    db_film = crud.get_film_title(db, title=film.title)
    if db_film:
        raise HTTPException(status_code=400, detail=f"Film with title `{film.title}` already registered")
    return crud.create_film(db=db, film=film)

# ==================================Company URLs===================================

@app.get("/companies/{id}/", response_model=schemas.CompanySchema)
def get_company(id: int, db: Session = Depends(get_db)):
    db_company = crud.get_company(db, id=id)
    if db_company is None:
        raise HTTPException(status_code=404, detail=f"Company with company id ({id}) not found")
    return db_company


@app.get("/companies/", response_model=list[schemas.CompanySchema])
def get_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_companies(db, skip=skip, limit=limit)


@app.post("/companies/", response_model=schemas.CompanySchema, status_code=status.HTTP_201_CREATED)
def create_company(company: schemas.CompanyCreateSchema, db: Session = Depends(get_db)):
    db_company = crud.get_company_by_name(db, name=company.name)
    if db_company:
        raise HTTPException(status_code=400, detail=f"Company with name `{company.name}` already exist, try editing")
    return crud.create_company(db=db, company=company)


#  response_model_exclude={'role'}, response_model_by_alias=Fals
# @app.put("/companies/{id}/", response_model=schemas.CompanyUpdate)
# def update_company(company: schemas.CompanyUpdateSchema, db: Session = Depends(get_db)):
#     # TODO
#     db_company = crud.update_company(db, email=company.email)
#     if db_company:
#         raise HTTPException(status_code=400, detail=f"Company with email `{company.email}` already registered")
#     return crud.create_company(db=db, company=company)

# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
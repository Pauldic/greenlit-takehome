from sqlalchemy.orm import Session, joinedload

from . import models, schemas

def get_user(db: Session, id: int):
    # return db.query(models.User).filter(models.User.id == id).first()
    return db.query(models.User).options(joinedload(models.User.films)).where(models.User.id == id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).options(joinedload(models.User.films)).where(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(models.User).offset(skip).limit(limit).all()
    return db.query(models.User).options(joinedload(models.User.films)).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        minimun_fee=user.minimun_fee)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.UserUpdate):
    db_user = models.User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        minimun_fee=user.minimun_fee)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_film(db: Session, id: int):
    # return db.query(models.Film).filter(models.Film.id == id).first()
    return db.query(models.Film).options(joinedload(models.Film.crew_members)).where(models.Film.id == id).first()


def get_films(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(models.Film).offset(skip).limit(limit).all()
    return db.query(models.Film).options(joinedload(models.Film.crew_members)).all()


def create_film(db: Session, film: schemas.FilmCreate):
    # TODO
    db_film = models.Film(
        first_name=film.first_name,
        last_name=film.last_name,
        email=film.email,
        minimun_fee=film.minimun_fee)
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film


def update_film(db: Session, film: schemas.FilmCreate):
    # TODO
    db_film = models.Film(
        first_name=film.first_name,
        last_name=film.last_name,
        email=film.email,
        minimun_fee=film.minimun_fee)
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film


def get_company(db: Session, id: int):
    # return db.query(models.Company).filter(models.Company.id == id).first()
    return db.query(models.Company).options(joinedload(models.Company.crew_members)).where(models.Company.id == id).first()


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(models.Company).offset(skip).limit(limit).all()
    return db.query(models.Company).options(joinedload(models.Company.crew_members)).all()


def create_company(db: Session, company: schemas.CompanyCreate):
    # TODO
    db_company = models.Company(
        first_name=company.first_name,
        last_name=company.last_name,
        email=company.email,
        minimun_fee=company.minimun_fee)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def update_company(db: Session, company: schemas.CompanyUpdate):
    # TODO
    db_company = models.Company(
        first_name=company.first_name,
        last_name=company.last_name,
        email=company.email,
        minimun_fee=company.minimun_fee)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

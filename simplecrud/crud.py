from sqlalchemy.orm import Session, joinedload

from simplecrud.models import Company
from . import models, schemas

def get_user(db: Session, id: int):
    # return db.query(models.User).filter(models.User.id == id).first()
    return db.query(models.User).options(joinedload(models.User.films)).options(joinedload(models.User.companies)).where(models.User.id == id).first()


def get_user_by_email(db: Session, email: str):
    # return db.query(models.User).filter(models.User.email == email).first()   # 0.065
    return db.query(models.User).options(joinedload(models.User.films)).options(joinedload(models.User.companies)).where(models.User.email == email).first()    # 0.068


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).options(joinedload(models.User.films)).options(joinedload(models.User.companies)).offset(skip).limit(limit).all()


def get_users_by_ids(db: Session, ids: list, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.id__in == ids).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreateSchema):
    db_user = models.User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            minimun_fee=user.minimun_fee
        )
    db.add(db_user)
    db.flush()
    
    films = []
    for obj in user.films:
        films.append(
            models.Film(
                title=obj.film.title,
                description=obj.film.description,
                budget=obj.film.budget,
                release_year=obj.film.release_year,
                genres=obj.film.genres
            )
        )
    if len(films) > 0:
        db.add_all(films)
        db.flush()

    print('Film Ids: ', list(map(lambda x: x.id, films)))
    crew_members = []
    for i, film in enumerate(films):
        crew_members.append(
            models.FilmCrewMembers(
                user_id=db_user.id,
                film_id=film.id,
                role=user.films[i].role
            )
        )
    if len(crew_members) > 0:
        db.add_all(crew_members)
        db.flush()

    companies = []
    for obj in user.companies:
        companies.append(
            models.Company(
                name=obj.company.name,
                contact_email_address=obj.company.contact_email_address,
                phone_number=obj.company.phone_number
            )
        )
    if len(companies) > 0:
        db.add_all(companies)
        db.flush()

    company_staff = []
    for i, company in enumerate(companies):
        company_staff.append(
            models.CompanyStaff(
                user_id=db_user.id,
                company_id=company.id,
                role=user.companies[i].role
            )
        )
    if len(company_staff) > 0:
        db.add_all(company_staff)
        db.flush()
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_post(db: Session, user: schemas.UserUpdateSchema):
    userUpdate = user.model_dump()
    userUpdate.pop('films', None)
    userUpdate.pop('companies', None)
    
    db.query(models.User).filter(models.User.id == user.id).update(userUpdate)
    db.flush()
    current_film_ids = []
    films = []
    for obj in user.films:
        if obj.film.id:
            # Updating the exisiting Linked Model for the m2m
            db.query(models.Film).filter(models.Film.id == obj.film.id).update(obj.film.dict())
            current_film_ids.append(obj.film.id)
            db.query(models.FilmCrewMembers).filter(models.FilmCrewMembers.film_id == obj.film.id, models.FilmCrewMembers.user_id == user.id).update({"role": obj.role})
        else:
            # Rebuilding list instance of the newly added link models in order to retain the list order
            film = models.Film(
                title=obj.film.title,
                description=obj.film.description,
                budget=obj.film.budget,
                release_year=obj.film.release_year,
                genres=obj.film.genres
            )
            films.append({"role": obj.role, "film": film})
    
    # If there are new films added (Save them)
    if len(films) > 0:
        new_films = list(map(lambda x: x["film"], films))
        db.add_all(new_films)
        db.flush()
        crew_members = []
        for i, film in enumerate(new_films):
            crew_members.append(
                models.FilmCrewMembers(
                    user_id=user.id,
                    film_id=film.id,
                    role=films[i]["role"]
                )
            )
        db.add_all(crew_members)
        db.flush() 
        current_film_ids += list(map(lambda x: x.film_id, crew_members))
    
    print('===> ', current_film_ids)
    db.flush()
    query = db.query(models.FilmCrewMembers).filter(models.FilmCrewMembers.user_id==user.id, ~models.FilmCrewMembers.film_id.in_(current_film_ids))
    query.delete(synchronize_session=False)
    db.flush()
    
    current_company_ids = []
    companies = []
    for obj in user.companies:
        if obj.company.id:
            # Updating the exisiting Linked Model for the m2m
            db.query(models.Company).filter(models.Company.id == obj.company.id).update(obj.company.dict())
            current_company_ids.append(obj.company.id)
            db.query(models.CompanyStaff).filter(models.CompanyStaff.company_id == obj.company.id, models.CompanyStaff.user_id == user.id).update({"role": obj.role})
        else:
            # Rebuilding list instance of the newly added link models in order to retain the list order
            company = models.Company(
                name=obj.company.name,
                contact_email_address=obj.company.contact_email_address,
                phone_number=obj.company.phone_number
            )
            companies.append({"role": obj.role, "company": company})
    
    # If there are new companies added (Save them)
    if len(companies) > 0:
        new_companies = list(map(lambda x: x["company"], companies))
        db.add_all(new_companies)
        db.flush()
        staff = []
        for i, company in enumerate(new_companies):
            staff.append(
                models.CompanyStaff(
                    user_id=user.id,
                    company_id=company.id,
                    role=companies[i]["role"]
                )
            )
        db.add_all(staff)
        db.flush()
        current_company_ids += list(map(lambda x: x.company_id, staff))

    query = db.query(models.CompanyStaff).filter(models.CompanyStaff.user_id==user.id, ~models.CompanyStaff.company_id.in_(current_company_ids))
    query.delete(synchronize_session=False)
    
    db.commit()
    return db.query(models.User).get(user.id)
        

def update_user_put(db: Session, user: schemas.UserUpdatePartial):
    # TODO: Implement Partial Update
    userUpdate = user.model_dump()
    print('User 1: ', userUpdate)
    userUpdate.pop('films', None)
    userUpdate.pop('companies', None)
    
    print('User 2: ', userUpdate)
    db.query(models.User).filter(models.User.id == user.id).update(userUpdate)
    db.flush()
    return db.query(models.User).get(user.id)
        
        
    # query.get() returns the models.User
    # db_user = db.query(models.User).get(user.id).instance_update(user)
    # db.commit()
    # db.refresh(db_user)
    # return db_user



def get_film(db: Session, id: int):
    # return db.query(models.Film).filter(models.Film.id == id).first()
    return db.query(models.Film).options(joinedload(models.Film.crew_members)).where(models.Film.id == id).first()

def get_film_title(db: Session, title: str):
    return db.query(models.Film).filter(models.Film.title == title).first()
    
def get_films(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(models.Film).offset(skip).limit(limit).all()
    return db.query(models.Film).options(joinedload(models.Film.crew_members)).all()


def get_films_by_ids(db: Session, ids: list, skip: int = 0, limit: int = 100):
    return db.query(models.Film).filter(models.Film.id.in_(ids)).offset(skip).limit(limit).all()


def create_film(db: Session, film: schemas.FilmCreateSchema):
    # TODO:
    # db_company = models.Company(
    #     name=film.company.name,
    #     contact_email_address=film.company.contact_email_address,
    #     phone_number=film.company.phone_number
    # )
    # db.add(db_company)
    # db.flush()
    
    db_film = models.Film(
            title=film.title,
            description=film.description,
            budget=film.budget,
            release_year=film.release_year,
            genres=film.genres,
            company_id = film.company_id
        )
    db.add(db_film)
    
    db.commit()
    db.refresh(db_film)
    return db_film


def update_film(db: Session, film: schemas.FilmCreateSchema):
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
    return db.query(models.Company).options(joinedload(models.Company.staff)).options(joinedload(models.Company.films)).where(models.Company.id == id).first()


def get_company_by_name(db: Session, name: str):
    return db.query(models.Company).filter(models.Company.name == name).first()


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).options(joinedload(models.Company.staff)).offset(skip).limit(limit).all()


def create_company(db: Session, company: schemas.CompanyCreateSchema):
    print('Company: ', company)
    db_company = models.Company(
            name=company.name,
            contact_email_address=company.contact_email_address,
            phone_number=company.phone_number
        )
    db.add(db_company)
    db.flush()
    
    
    films = []
    for film in company.films:
        films.append(
            models.Film(
                title=film.title,
                description=film.description,
                budget=film.budget,
                release_year=film.release_year,
                genres=film.genres,
                company_id=film.company_id
            )
        )
    if len(films) > 0:
        db.add_all(films)
        db.flush()
    
    # TODO: 
    return db_company


def update_company(db: Session, company: schemas.CompanyUpdateSchema):
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

from pydantic import BaseModel as _BaseModel, root_validator, EmailStr, Field, PositiveInt, validator
from pydantic.fields import FieldInfo
# from pydantic.utils import GetterDict
from pydantic._internal._model_construction import ModelMetaclass
from typing import Literal, Optional, Tuple, Dict, Any, Generic, Type, TypeVar
from pydantic_partial import PartialModelMixin, create_partial_model

# from enum import Enum
import datetime
from simplecrud.models import Film

    
class BaseModel(PartialModelMixin, _BaseModel):
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed=True
        # populate_by_name = True
        

class UserBase(BaseModel):
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    minimun_fee: PositiveInt


class UserCreateSimple(UserBase):
    # In case this will be used for signin, we might not want to make it editable
    email: EmailStr


class UserUpdateFull(UserBase):
    id: int

class UserUpdatePartial(BaseModel):
    id: int
    first_name: Optional[str] = Field(max_length=64, required=False)
    last_name: Optional[str] = Field(max_length=64, required=False)
    minimun_fee: Optional[PositiveInt]


class User(UserBase):
    id: int
    email: EmailStr
      

class CompanyBase(BaseModel):
    name: str = Field(max_length=32)
    contact_email_address: EmailStr
    phone_number: str = Field(max_length=15)
    

class CompanyCreateSimple(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    id: int | None = 0


class CompanyUpdatePartial(BaseModel):
    id: int
    name: Optional[str] = Field(max_length=32)
    contact_email_address: Optional[str] = EmailStr
    phone_number: Optional[str] = Field(max_length=15)


class Company(CompanyBase):
    id: int


class FilmBase(BaseModel):
    title: str = Field(max_length=32)
    description: str | None = None
    budget: PositiveInt
    release_year: int
    genres: list[str] | None = []
    company_id: int | None = 0
    
    @validator("release_year")
    def valid_year(cls, v):
        this_year = datetime.date.today().year
        if v < 1900 or v > this_year:
            raise ValueError(f"Year must be a valid year between 1900 to {this_year}")
        return v

    
class FilmCreateSimple(FilmBase):
    pass
    
      
class FilmUpdate(FilmBase):
    id: int | None = 0
     
     
class FilmUpdatePartial(BaseModel):
    id: int | None = 0
    title: Optional[str] = Field(max_length=32)
    description: Optional[str] | None = None
    budget: Optional[PositiveInt]
    release_year: Optional[int]
    genres: list[str] | None = []
    company_id: int | None = 0
     
    @validator("release_year")
    def valid_year(cls, v):
        this_year = datetime.date.today().year
        if v < 1900 or v > this_year:
            raise ValueError(f"Year must be a valid year between 1900 to {this_year}")
        return v

    
class Film(FilmBase):
    id: int
   

class RelatedUserSchema(UserBase):
    id: int
    email: EmailStr

class RelatedCompanySchema(CompanyBase):
    id: int

class RelatedFilmSchema(FilmBase):
    id: int


# ========================== Associations =============================


# users and films have a many to many relationship where the role of the user can be either “writer”, “producer”, or “director”
# users and companies have a many to many relationship where the role is “owner” or “member”
# companies and films have a one to may relationship


class UserCompanySchema(BaseModel):
    role: Literal['owner', 'member']
    company: RelatedCompanySchema

class CompanyUserSchema(BaseModel):
    role: Literal['owner', 'member']
    user: RelatedUserSchema

class UserFilmSchema(BaseModel):
    role: Literal['director', 'producer', 'writer']
    film: RelatedFilmSchema

class FilmUserSchema(BaseModel):
    role: Literal['director', 'producer', 'writer']
    user: RelatedUserSchema


class UserSchema(User):
    films: list[UserFilmSchema] # n-n
    companies: list[UserCompanySchema]  # n-n

class CompanySchema(Company):
    films: list[Film]   # 1-n reverse
    staff: list[CompanyUserSchema]  # n-n

class FilmSchema(Film):
    crew_members: list[FilmUserSchema]  # n-n


# ================ Create Schemas ===============


class UserCompanyCreateSchema(BaseModel):
    role: Literal['owner', 'member']
    company: CompanyCreateSimple

class CompanyUserCreateSchema(BaseModel):
    role: Literal['owner', 'member']
    user: UserCreateSimple

class UserFilmCreateSchema(BaseModel):
    role: Literal['director', 'producer', 'writer']
    film: FilmCreateSimple

class FilmUserCreateSchema(BaseModel):
    role: Literal['director', 'producer', 'writer']
    user: UserCreateSimple


class UserCreateSchema(UserCreateSimple):
    films: list[UserFilmCreateSchema] | None = [] # n-n
    companies: list[UserCompanyCreateSchema] | None = []  # n-n

class CompanyCreateSchema(CompanyCreateSimple):
    films: list[Film] | None = []   # 1-n reverse
    staff: list[CompanyUserCreateSchema] | None = []  # n-n

class FilmCreateSchema(FilmCreateSimple):
    crew_members: list[FilmUserCreateSchema] | None = []  # n-n


# ================ Update Schemas ===============


class UserCompanyUpdateSchema(BaseModel):
    role: Literal['owner', 'member']
    company: CompanyUpdate

class CompanyUserUpdateSchema(BaseModel):
    role: Literal['owner', 'member']
    user: UserUpdateFull

class UserFilmUpdateSchema(BaseModel):
    role: Literal['director', 'producer', 'writer']
    film: FilmUpdate

class FilmUserUpdateSchema(BaseModel):
    role: Literal['director', 'producer', 'writer']
    user: UserUpdateFull


class UserUpdateSchema(UserUpdateFull):
    films: list[UserFilmUpdateSchema] | None = [] # n-n
    companies: list[UserCompanyUpdateSchema] | None = []  # n-n

class CompanyUpdateSchema(CompanyUpdate):
    films: Optional[list[Film]] | None = []   # 1-n reverse
    staff: Optional[list[CompanyUserUpdateSchema]] | None = []  # n-n

class FilmUpdateSchema(Film):
    crew_members: list[FilmUserUpdateSchema] | None = []  # n-n

# ============ Partial Update ===============
# https://github.com/pydantic/pydantic/issues/6381/

UserUpdatePartialSchema = UserUpdateSchema.model_as_partial()


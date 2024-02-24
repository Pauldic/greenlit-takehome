from pydantic import BaseModel as _BaseModel, EmailStr, Field, PositiveInt, validator
from typing import Literal, Annotated
from enum import Enum
import datetime


class BaseModel(_BaseModel):
    
    class Config:
        from_attributes = True
        populate_by_name = True
        
        
class FilmRoles(str, Enum):
    WRITER = 'writer'
    PRODUCER = 'producer'
    DIRECTOR = 'director'
        
class CompanyRoles(str, Enum):
    WRITER = 'writer'
    PRODUCER = 'producer'
    DIRECTOR = 'director'
    
    
class UserBase(BaseModel):
    # Common
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    email: EmailStr
    minimun_fee: PositiveInt
    # role: str | None = None
    # role: Literal['possible_value_1', 'possible_value_2']


class UserCreate(UserBase):
    pass


class UserUpdate(UserCreate):
    id: int


class User(UserBase):
    id: int
        

class CompanyBase(BaseModel):
    # Common
    name: str = Field(max_length=32)
    contact_email_address: EmailStr
    phone_number: str = Field(max_length=15)
    role: str | None = None
    

class UserRole(User):
    user_id: int
    role: Literal['owner', 'member']
    
class CompanyCreate(CompanyBase):
    # Create
    staff: list[UserRole]
    film_ids: list[int]


class CompanyUpdate(CompanyCreate):
    id: int

class Company(CompanyBase):
    id: int
    # film_ids: list[int] = []


class FilmBase(BaseModel):
    # Common
    title: str = Field(max_length=32)
    description: str | None = None
    budget: PositiveInt
    release_year: int
    genres: list[str] | None = []
    role: str | None = None

    @validator("release_year")
    def valid_year(cls, v):
        this_year = datetime.date.today().year
        if v < 1900 or v > this_year:
            raise ValueError(f"Year must be a valid year between 1900 to {this_year}")
        return v

class FilmCreate(FilmBase):
    # Create
    company_id: int
    user_role: list[str]
    
    class Config:
        populate_by_name = True # For Proxy
        from_attributes = True  
        use_enum_values = True  # For Enum


class Film(FilmBase):
    id: int
    company: Company
   


class UserSchema(User):
    films: list[Film]
    companies: list[Company]


class CompanySchema(Company):
    films: list[Film]
    staff: list[User]


class FilmSchema(Film):
    crew_members: list[User]

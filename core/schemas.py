from pydantic import BaseModel


class UserBase(BaseModel):
    # Common
    first_name: str
    last_name: str
    email: str
    minimun_fee: int | None = 0
    role: str | None = None


class UserCreate(UserBase):
    # Create
    pass


class User(UserBase):
    # Read
    id: int

    class Config:
        from_attributes = True


class CompanyBase(BaseModel):
    # Common
    name: str
    contact_email_address: str
    phone_number: str
    


class CompanyCreate(CompanyBase):
    # Create
    pass


class Company(CompanyBase):
    id: int
    # film_ids: list[int] = []

    class Config:
        from_attributes = True


class FilmBase(BaseModel):
    # Common
    title: str
    description: str | None = None
    budget: int | None = 0
    release_year: int
    # genres: list[str] | []


class FilmCreate(FilmBase):
    # Create
    company_id: int


class Film(FilmBase):
    id: int
    company: Company

    class Config:
        from_attributes = True
        


class UserSchema(User):
    films: list[Film]
    companies: list[Company]


class ComapnySchema(Company):
    films: list[Film]
    staff: list[User]


class FilmSchema(Film):
    crew_members: list[User]

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType

from .database import Base


class FilmCrewMembers(Base):
    __tablename__ = 'user_film'
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    film_id = Column(ForeignKey('films.id'), primary_key=True)
    role = Column(String(16), nullable=False)
    film = relationship("Film", back_populates="crew_members")
    user = relationship("User", back_populates="films")


class CompanyStaff(Base):
    __tablename__ = 'company_user'
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    company_id = Column(ForeignKey('companies.id'), primary_key=True)
    role = Column(String(16), nullable=False)
    company = relationship("Company", back_populates="staff")
    user = relationship("User", back_populates="companies")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), index=True)
    last_name = Column(String(64), index=True)
    email = Column(String(254), index=True)
    minimun_fee = Column(Integer, default=0)
    # n-n reverse
    films = relationship(FilmCrewMembers, back_populates="user")
    companies = relationship(CompanyStaff, back_populates="user")


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True)
    title = Column(String(32), index=True, nullable=False)
    description = Column(String, nullable=True)
    budget = Column(Integer, index=True, default=0)
    release_year = Column(Integer, index=True, nullable=False)
    genres = Column(MutableList.as_mutable(PickleType), default=[])
    # Foreignkey Relation
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="films")
    # n-n reverse
    crew_members = relationship(FilmCrewMembers, back_populates="film")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, nullable=False)
    contact_email_address = Column(String(254), index=True)
    phone_number = Column(String(15), index=True)
    # 1-n reverse
    films = relationship("Film", back_populates="company") 
    # n-n reverse
    staff = relationship(CompanyStaff, back_populates="company") 
    
    # staff = relationship('User',
    #                       secondary=CompanyMembersAssociation,
    #                       back_populates='companies',
    #                       cascade='all, delete'
    #                 )
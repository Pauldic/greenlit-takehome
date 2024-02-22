from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType

from .database import Base

# “writer”, “producer”, or “director” extra membership role
UserFilmsAssociation = Table('user_film',
                    Base.metadata,
                    Column('user_id', Integer, ForeignKey('users.id')),
                    Column('film_id', Integer, ForeignKey('films.id'))
                )

#  “owner” or “member” extra membership role
CompanyMembersAssociation = Table('company_user',
                    Base.metadata,
                    Column('user_id', Integer, ForeignKey('users.id')),
                    Column('company_id', Integer, ForeignKey('companies.id'))
                )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), index=True)
    last_name = Column(String(64), index=True)
    email = Column(String(128), index=True)
    minimun_fee = Column(Integer, default=0)
    # role = Column(String(8), index=True)    
    
    films = relationship('Film',
                         secondary=UserFilmsAssociation,
                         back_populates='crew_members',
                         cascade='all, delete'
                    )

    companies = relationship('Company',
                         secondary=CompanyMembersAssociation,
                         back_populates='staff',
                         cascade='all, delete'
                    )


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True)
    title = Column(String(32), index=True, nullable=False)
    description = Column(String, nullable=True)
    budget = Column(Integer, index=True, default=0)
    release_year = Column(Integer, index=True, nullable=False)
    # genres = Column(MutableList.as_mutable(PickleType), default=[])
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="companies")
    
    crew_members = relationship('User',
                          secondary=UserFilmsAssociation,
                          back_populates='films',
                          cascade='all, delete'
                    )


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, nullable=False)
    contact_email_address = Column(String(128), index=True)
    phone_number = Column(String(15), index=True)
    
    films = relationship("Film", back_populates="films")
    
    staff = relationship('User',
                          secondary=CompanyMembersAssociation,
                          back_populates='companies',
                          cascade='all, delete'
                    )
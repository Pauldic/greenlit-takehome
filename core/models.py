from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, object_session
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from sqlalchemy.sql import text

from .database import Base

# “writer”, “producer”, or “director” extra membership role
# UserFilmsAssociation = Table('user_film',
#                     Base.metadata,
#                     Column('user_id', Integer, ForeignKey('users.id')),
#                     Column('film_id', Integer, ForeignKey('films.id'))
#                 )

#  “owner” or “member” extra membership role
# CompanyMembersAssociation = Table('company_user',
#                     Base.metadata,
#                     Column('user_id', Integer, ForeignKey('users.id')),
#                     Column('company_id', Integer, ForeignKey('companies.id'))
#                 )


class FilmCrewMembers(Base):
    __tablename__ = 'user_film'
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    film_id = Column(ForeignKey('films.id'), primary_key=True)
    role = Column(String(16), nullable=False)
    # proxies
    user = relationship("User", back_populates="films")
    film = relationship("Film", back_populates="crew_members")

class CompanyStaff(Base):
    __tablename__ = 'company_user'
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    company_id = Column(ForeignKey('companies.id'), primary_key=True)
    role = Column(String(16), nullable=False)
    # proxies
    user = relationship("User", back_populates="companies")
    company = relationship("Company", back_populates="staff")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), index=True)
    last_name = Column(String(64), index=True)
    email = Column(String(254), index=True)
    minimun_fee = Column(Integer, default=0)
    # n-n proxies reverse
    films = relationship(FilmCrewMembers, back_populates="user")
    companies = relationship(CompanyStaff, back_populates="user")
    
    # @property
    # def films(self):
    #     s = text(f"""
    #         SELECT temp.* FROM (
    #             SELECT
    #                 films.*,
    #                 user_film.role,
    #                 user_film.user_id
    #             FROM films INNER JOIN user_film ON films.id = user_film.film_id
    #         ) AS temp
    #         INNER JOIN users ON temp.user_id = users.id
    #         WHERE users.id = {self.id}
    #         """)
    #     # print('SQL: ', s)
    #     return object_session(self).execute(s).fetchall()
    
    # films = relationship('Film',
    #                      secondary=UserFilmsAssociation,
    #                      back_populates='crew_members',
    #                      cascade='all, delete'
    #                 )

    # @property
    # def companies(self):
    #     s = text(f"""
    #         SELECT temp.* FROM (
    #             SELECT
    #                 companies.*,
    #                 company_user.role,
    #                 company_user.user_id
    #             FROM companies INNER JOIN company_user ON companies.id = company_user.company_id
    #         ) AS temp
    #         INNER JOIN users ON temp.user_id = users.id
    #         WHERE users.id = {self.id}
    #         """)
    #     return object_session(self).execute(s).fetchall()
    
    # companies = relationship('Company',
    #                      secondary=CompanyMembersAssociation,
    #                      back_populates='staff',
    #                      cascade='all, delete'
    #                 )


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
    # n-n proxies reverse
    crew_members = relationship(FilmCrewMembers, back_populates="film")
    
    # @property
    # def crew_members(self):
    #     s = """
    #         SELECT temp.* FROM (
    #           SELECT
    #             users.*,
    #             user_film.role,
    #             user_film.film_id
    #           FROM users INNER JOIN user_film ON users.id = user_film.user_id
    #         ) AS temp
    #         INNER JOIN users ON temp.film_id = films.id
    #         WHERE films.id = :filmid
    #         """
    #     result = object_session(self).execute(s, params={'filmid': self.id}).fetchall()
        
    #     print('Crew Result: ', result)
    #     return result
    
    # crew_members = relationship('User',
    #                       secondary=UserFilmsAssociation,
    #                       back_populates='films',
    #                       cascade='all, delete'
    #                 )


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, nullable=False)
    contact_email_address = Column(String(254), index=True)
    phone_number = Column(String(15), index=True)
    # 1-n reverse
    films = relationship("Film", back_populates="company") 
    # n-n proxy reverse
    staff = relationship(CompanyStaff, back_populates="company") 
    
    # @property
    # def staff(self):
    #     s = """
    #         SELECT temp.* FROM (
    #           SELECT
    #             users.*,
    #             company_user.role,
    #             company_user.company_id
    #           FROM users INNER JOIN company_user ON users.id = company_user.user_id
    #         ) AS temp
    #         INNER JOIN users ON temp.company_id = companies.id
    #         WHERE companies.id = :companyid
    #         """
    #     result = object_session(self).execute(s, params={'companyid': self.id}).fetchall()
        
    #     print('Staff Result: ', result)
    #     return result
    
    # staff = relationship('User',
    #                       secondary=CompanyMembersAssociation,
    #                       back_populates='companies',
    #                       cascade='all, delete'
    #                 )
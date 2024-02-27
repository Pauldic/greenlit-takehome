from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Can define your own .env file in the project root (See .env.sample and rename to .env)
DB_SERVER = config("DB_SERVER", default="localhost")
DB_NAME = config("DB_NAME", default="")
DB_USER = config("DB_USER", default="")
DB_PASS = config("DB_PASS", default="")

SQLALCHEMY_POSTGRES_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_SERVER}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_POSTGRES_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Create the tables in the database
Base.metadata.create_all(engine)
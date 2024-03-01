from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

## environment 
load_dotenv()

## Local DB env
DB_TYPE=os.getenv("DB_TYPE")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")

if None in [DB_TYPE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]:
    raise ValueError("Some database environment variables are missing.")

Base = declarative_base()
local_engine = create_engine(f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", pool_size=100)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=local_engine)


def init_local_db():
    Base.metadata.create_all(bind=local_engine)

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

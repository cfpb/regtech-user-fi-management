import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import sessionmaker

ENV = os.getenv("ENV", "LOCAL")

if ENV == "LOCAL":
    load_dotenv("src/.env.local")
else:
    load_dotenv()

DATABASE_URL = os.environ.get("INST_CONN")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()

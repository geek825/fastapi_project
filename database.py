from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:12345@localhost:5433/daily" 
engine = create_engine(DATABASE_URL)

sessionlocal = sessionmaker(bind=engine)
Base = declarative_base()
        
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://expenses_db_041z_user:rjWxMFHHMYBZvCdIQvPJ6mQuWAKb5Z2T@dpg-d2dfujc9c44c73f6n6o0-a/expenses_db_041z" 

engine = create_engine(DATABASE_URL)

sessionlocal = sessionmaker(bind=engine)
Base = declarative_base()
        
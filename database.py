from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

<<<<<<< HEAD
DATABASE_URL = "postgresql://expenses_db_041z_user:rjWxMFHHMYBZvCdIQvPJ6mQuWAKb5Z2T@dpg-d2dfujc9c44c73f6n6o0-a/expenses_db_041z" 
=======
DATABASE_URL = "postgresql://postgres:12345@localhost:5433/daily" 
>>>>>>> origin/main
engine = create_engine(DATABASE_URL)

sessionlocal = sessionmaker(bind=engine)
Base = declarative_base()
        
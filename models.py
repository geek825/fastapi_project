from sqlalchemy import Column, Integer, String, ARRAY
from database import Base

class User(Base):
    __tablename__ = 'users'
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String(300), nullable=False)
    hobbies = Column(ARRAY(String))
    
class Userlog(Base):
    __tablename__ = "users"
    email = str
    password = str
    
    

    

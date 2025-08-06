from pydantic import BaseModel
from typing import List 

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    hobbies: List[str]

class Userlogin(BaseModel):
    # first_name: str
    # last_name: str
    email: str
    password : str
    # hobbies: List[str]

    class Config:
        from_attributes = True

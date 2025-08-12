from pydantic import BaseModel

from typing import List
from datetime import date

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

class Expense(BaseModel) :
    id : int
    amount : int 
    description : str
    category :str
    date : date
     
     
# class ExpenseUodate(BaseModel):
#     amount = int
#     description = str
#     category = str
#     date = date 
      

    class Config:
        from_attributes = True

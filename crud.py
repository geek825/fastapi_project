from sqlalchemy.orm import Session
from models import User as UserModel
from schema import UserCreate 
from auth import hash_password , verify_password 



def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = UserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        hobbies=user.hobbies,
        email=user.email,
        password= hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# def get_user(db: Session, email: str):
#     user_obj = db.query(UserModel).filter(UserModel.email == email).first()
#     if not user_obj:
#         return False
#     return user_obj


def user_auth(db: Session, email : str , password: str):
    user_obj = db.query(UserModel).filter(UserModel.email == email).first()
    if not user_obj:
        return False
    if not verify_password():
        return None
    return user_obj


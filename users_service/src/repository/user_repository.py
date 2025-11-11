from pydantic import EmailStr
from sqlalchemy.orm import Session

from model.user_model import User
from service.dto.user_dto import UserCreate


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_email(db: Session, email: EmailStr):
    return db.query(User).filter(User.email == email).first()


def add_user(db: Session, user: UserCreate):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    return new_user

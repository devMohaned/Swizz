from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from db.database import get_db
from security.jwt_auth import get_current_user
from service import user_service
from service.authorization_service import authorize_request
from service.dto.user_dto import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
async def get_users(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    await authorize_request(request, role=user["role"], sub=user["sub"])
    return user_service.get_users(db)


@router.post("/", response_model=UserResponse)
async def add_user(request: Request, new_user: UserCreate, db: Session = Depends(get_db),
                   user=Depends(get_current_user)):
    await authorize_request(request, role=user["role"], sub=user["sub"])
    return user_service.create_user(db, new_user)

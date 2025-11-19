from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .schemas import UserCreate, UserOut
from .utils import hash_password

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.username == user.username).first()
    if exists:
        raise HTTPException(400, "User already exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password),
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

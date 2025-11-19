from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .auth import get_db, get_current_user, require_admin
from .models import User
from .utils import verify_password, create_access_token
from .users import router as user_router
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/admin")
def admin_route(user: User = Depends(require_admin)):
    return {"msg": "Welcome Admin"}

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.databace import get_db
from app.users.models import User
from app.users.auth import create_access_token, get_current_user
from fastapi.responses import Response
from app.users.schemas import UserSchema
from app.users.auth import verify_token,oauth2_scheme
auth = APIRouter(prefix="/auth",tags=["Auth"])


@auth.post("/register")
async def user_register(user: UserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        return {"message": "User Already Exists"}

    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User Created"}


@auth.post("/login")
async def user_login(user: UserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if not existing_user:
        return {"message": "User Not Found"}
    if existing_user.password != user.password:
        return {"message": "Username or Password Incorrect"}
    access_token = create_access_token(data={"sub": user.username})
    return {"message": "User Login Succesfuly", "access_token": access_token, "token_type": "bearer"}


@auth.get("/auth/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    return verify_token(token)


@auth.get("/logout")
async def logout(response: Response, current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    response.delete_cookie(key="access_token")
    return {"message": "User Logout Succesfuly"}

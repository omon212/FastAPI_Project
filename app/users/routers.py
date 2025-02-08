from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.databace import get_db
from app.users.models import User
from app.users.auth import create_access_token, oauth2_scheme, verify_token
from fastapi.responses import Response
from app.users.schemas import UserSchema
from app.users.auth import blacklisted_tokens, revoke_access_token

auth = APIRouter(prefix="/auth", tags=["Auth"])


@auth.post("/register", status_code=200)
async def user_register(user: UserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        return {"message": "User Already Exists"}

    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User Created"}


@auth.post("/login", status_code=200)
async def user_login(user: UserSchema, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username == user.username).first()
    if not existing_user:
        return {"message": "User Not Found"}
    if existing_user.password != user.password:
        return {"message": "Username or Password Incorrect"}

    access_token = create_access_token(data={"username": user.username})
    return {"message": "User Login Successfully", "access_token": access_token, "token_type": "bearer"}


@auth.get("/me", status_code=200)
def read_users_me(token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return verify_token(token)


@auth.post("/logout", status_code=200)
async def logout(response: Response, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Not authenticated")

    revoke_access_token(token)
    response.delete_cookie("access_token")
    return {"message": "User Logged Out Successfully"}

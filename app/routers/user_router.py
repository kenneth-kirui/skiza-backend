from typing import Optional
from fastapi import APIRouter, Depends,status, HTTPException
from fastapi.params import Body
from sqlalchemy.orm import Session
from ..database import  crud
from ..dependencies import dependencies
from ..pydantics import user
from .shared_scripts.scripts import get_password_hash, get_current_user

router = APIRouter(
    tags=['Users'],
    prefix="/users"
)

@router.post("/", response_model=user.UserCreate)
def create_user(payload:dict = Body(...), db: Session = Depends(dependencies.get_db)):
    user_data = user.UserCreate(
        firstname=payload.get('firstname'),
        lastname=payload.get('lastname').lower(),
        email=payload.get('email').lower(),
        password=get_password_hash(payload.get('password')),
        role_id=payload.get('role_id')
    )
    user_in_db = crud.get_user_by_email(db=db, email=user_data.email)
    if user_in_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user with emial {user_data.email} already exist")
    db_user = crud.create_user(db, user_data)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid data provided!")
    return db_user

@router.get("/", response_model=list[user.UserInDB])
def read_users(skip: int = 0, limit: int = 10,searchText:Optional[str]='', db: Session = Depends(dependencies.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit, search =searchText)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"No users found"})
    return users

@router.get("/{user_id}", response_model=user.UserInDB)
def read_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"User not found!"})
    return db_user

@router.put("/{user_id}", response_model=user.UserUpdate)
def update_user(user_id: int, user_update: user.UserUpdate, db: Session = Depends(dependencies.get_db), user_data = Depends(get_current_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"User not found!"})
    if user_update.password:
        hashed_password = get_password_hash(user_update.password)
        user_update.password = hashed_password

    updated_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    return updated_user

@router.delete("/{user_id}", response_model=user.UserInDB)
def delete_user(user_id: int, db: Session = Depends(dependencies.get_db), user_data = Depends(get_current_user)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"User not found!"})
    return db_user
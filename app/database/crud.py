from typing import Optional
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from . import models
from ..pydantics.user import UserCreate, UserUpdate 
from ..pydantics.tune import TuneCreate, TuneUpdate

#user operations
def create_user(db:Session, user: UserCreate):
  hashed_password = user.password
  db_user = models.User(firstname = user.firstname, lastname = user.lastname, email=user.email, password = hashed_password, role_id = user.role_id)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10, search:Optional[str]=''):
    query = db.query(models.User) 
    if search:
        query = query.filter(models.User.firstname.ilike(f'%{search}%'))
    return query.offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None

#create tune
def create_tune(db:Session, tune: TuneCreate):
    db_tune = models.Tune(name = tune.name, code = tune.code, file_name = tune.file_name, user_id=tune.user_id)
    db.add(db_tune)
    db.commit()
    db.refresh(db_tune)
    return db_tune

#get all tunes
def get_tunes(db:Session, skip: int = 0, limit: int = 100, search:Optional[str]= ''):
     return db.query(models.Tune).filter(models.Tune.name.contains(search)).offset(skip).limit(limit).all()

def get_tune(db:Session, tune_id:int):
    return db.query(models.Tune).filter(models.Tune.id==tune_id)

# Delete tune
def delete_tune(db:Session, tune_id:int):
    db_tune = db.query(models.Tune).filter(models.Tune.id == tune_id).first()
    if db_tune:
        db.delete(db_tune)
        db.commit()
    return None
#updatetune
def update_tune(db: Session, id: int, tune:TuneUpdate) -> models.Tune:
    tune_query = db.query(models.Tune).filter(models.Tune.id == id)
    tune_in_db = tune_query.first()
    if tune_in_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Tune not found"})
    
    tune_query.update(tune.dict(), synchronize_session=False)
    db.commit()
    
    updated_tune = tune_query.first()
    db.refresh(updated_tune)
    
    return updated_tune


    

    
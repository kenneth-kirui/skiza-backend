from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import crud
from ..pydantics import user
from ..dependencies.dependencies import get_db
from ..routers.shared_scripts.scripts import  create_access_token, verify_password
from ..core.config import settings

ALGORITHIM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY
router = APIRouter()

router = APIRouter(
    tags=['Auth'],
)

@router.post("/login")
async def login(user_credentials:user.UserLogin, db:Session = Depends(get_db) ):
  user = crud.get_user_by_email(db,user_credentials.email.lower())
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Invalid credentials")
  if not verify_password(user_credentials.password, user.password):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Invalid credentials")
  accsess_token = create_access_token(data ={"user_id": user.id, "user_role":user.role_id})
  return {"access_token": accsess_token, "token_type":"bearer","user_role":user.role_id,  "user_id":user.id}


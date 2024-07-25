from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from ...core.config import settings
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key #"d963346e21281c663b756f17a767b8e64d2664b70c6e4dc5d0d9e9dd7f14f69c"
ALGORITHM = settings.algorithm #"HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
  return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else: 
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp":expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
  return encoded_jwt

def verify_access_token(token: str, credentials_exception):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

    id: str = payload.get("user_id")
    role: int = payload.get("role_id")

    if id is None:
      raise credentials_exception
    
    token_data= {"id": id, "role": role}
  except JWTError:
    raise credentials_exception
  
  return token_data
  
def get_current_user(token:str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials", headers = {"WWW-Authenticate": "Bearer"})

  return verify_access_token(token, credentials_exception)
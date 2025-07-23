from fastapi.security import OAuth2PasswordBearer
from cryptography.fernet import Fernet
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from typing import Annotated
from schemas import UserToken
import database as Db
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "ASIRI_GIZLI_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "HZeIwfGpOyd5YRrr-pYp3seH7bXWMTusQguXdTgnvzo=").encode()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
f = Fernet(ENCRYPTION_KEY) 

def verify_password(user_password, hashed_password):
    return pwd_context.verify(user_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def decrypt_embedding(encrypted_embedding: bytes) -> list:
    """Şifreli veriyi çözüp embedding listesine dönüştürür."""
    decrypted_str = f.decrypt(encrypted_embedding).decode('utf-8')
    embedding_list = list(map(float, decrypted_str.split(',')))
    return embedding_list

def encrypt_embedding(embedding: list) ->bytes:
    """Embedding listesini string'e çevirip şifreler."""
    # Listeyi -> String -> Bytes -> Şifreli Bytes
    embedding_str = ",".join(map(str, embedding))
    encrypted_data = f.encrypt(embedding_str.encode('utf-8'))
    return encrypted_data

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_decode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_decode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_decode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        username: str = payload.get("sub")
        if username is None:
        
            raise credentials_exception
        
    except InvalidTokenError as e:
        
        raise credentials_exception
    user = Db.get_user(username)
    if user is None:
        
        raise credentials_exception
    
    return user

async def get_current_admin_user(current_user: Annotated[dict, Depends(get_current_user)]):
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu işlemi yapmak için admin yetkisi gereklidir."
        )
    return current_user



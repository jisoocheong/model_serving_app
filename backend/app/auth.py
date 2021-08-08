import security 

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status

from config import settings as global_config
from security import verify_password
from model_serving_db.schemas import TokenData, User
from model_serving_db.crud import get_user, create_user


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def sign_up_new_user(username: str, email: str, password: str):
    user = get_user(username)
    if user:
        return False  # User already exists
    
    new_user = create_user(username, email, password)
    return new_user


async def get_current_user(
    token: str = Depends(security.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, global_config.secret_key, algorithms=[global_config.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


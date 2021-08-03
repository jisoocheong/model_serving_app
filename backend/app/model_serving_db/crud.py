import psycopg2

from fastapi import Depends

from app.config import Settings, get_settings
from app.security import get_password_hash
from .schemas import UserInDB
from .creators import create_model_serving_db, create_user_table



def get_user(username: str, settings: Settings = Depends(get_settings)):
    # connect to database and get user
    
    host = settings.database_host
    port = settings.database_port
    
    # ...
    # ...
    # ...
    existing_user = cursor.fetchone()
    
    # return user
    return UserInDB({
        "username": existing_user[1],
        "email": existing_user[2],
        "hashed_password": existing_user[3]
    })


def create_user(username: str, email: str, password: str, settings: Settings = Depends(get_settings)):
    # connect to database and add user
    
    host = settings.database_host
    port = settings.database_port
    
    hashed_password = get_password_hash(password)
    
    # ...
    # ...
    # ...
    
    existing_user = cursor.fetchone()
    
    # return user
    return UserInDB({
        "username": existing_user[1],
        "email": existing_user[2],
        "hashed_password": existing_user[3]
    })
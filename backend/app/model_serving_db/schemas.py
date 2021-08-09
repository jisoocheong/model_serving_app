from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    # full_name: Optional[str] = None
    # disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class Model(BaseModel):
    username: str
    framework: str
    name: str
    version: str
    size: str
    device_dep: list
    description: str
    tags: list
    input: str
    output: str
    test_code: str
    screenshot: list
    model_files: str 

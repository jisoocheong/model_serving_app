from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.model_serving_db import user_table
from pydantic import BaseModel
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional
import os
from fastapi.security import OAuth2PasswordBearer


class LoginBody(BaseModel):
    username: str
    password: str

class NewUserBody(BaseModel):
    email: str
    username: str
    first_password: str
    second_password: str

class Token(BaseModel):
    access_token: str
    token_type: str



app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
load_dotenv() # read the env var from .env file


origins = [
        "http://localhost:3000",
        "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Takes in information in data and returns a tokenized version of it. It also has the 
    option of including the expiration time of the token
    """
    to_encode = data.copy() 
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    secret_key = os.environ.get("secret")
    alg = os.environ.get("algorithm")    
    token = jwt.encode(to_encode, secret_key, alg)
    return token



@app.get("/")
@app.get("/index")
async def read_root():
    #Add logic for users already logged in
    return {"data": "some data"}




@app.post("/")
@app.post("/index")
async def login(body:LoginBody):
    #add logic for checking user input
    login_status = user_table.check_valid_login(body.username, body.password)


    access_token_expires = timedelta(minutes=os.environ.get("access_token_expire_minutes"))
    access_token = create_access_token(body, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

"""
    secret = os.environ.get("secret")
    alg = os.environ.get("algorithm")    
    token = jwt.encode({"result": login_status}, secret, alg)
    return {"token":token}
"""
    #return make_response("could not verify", 401, {"Authentication", "login required"})


@app.get("/search")
async def search():
    return {"data": "This should show a page with a search bar"}



@app.get("/create")
async def get_create():
    return {"data" : "A page for a new user to be born"}



@app.post("/create")
async def post_create(body: NewUserBody):
    added_new_user = False
    if body.first_password == body.second_password:
        added_new_user = user_table.add_user(body.username, body.email, body.first_password)
    return {"result": added_new_user} 






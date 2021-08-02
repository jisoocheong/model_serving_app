from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.model_serving_db import user_table
from pydantic import BaseModel
import jwt
from dotenv import load_dotenv
import os


class LoginBody(BaseModel):
    username: str
    password: str


class NewUserBody(BaseModel):
    email: str
    username: str
    first_password: str
    second_password: str


app = FastAPI()


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
    secret = os.environ.get("secret")
    alg = os.environ.get("algorithm")    
    token = jwt.encode({"result": login_status}, secret, alg)
    return {"token":token}

    #return make_response("could not verify", 401, {"Authentication", "login required"})


@app.get("/search")
async def search():
    return {"data": "This should show a page with a search bar"}



@app.get("/create")
async def get_create():
    return {"data" : "A page for a new user to be born"}



@app.post("/create")
async def post_create(body: NewUserBody):
    added_new_user = True
    if body.first_password == body.second_password:
        added_new_user = user_table.add_user(body.username, body.email, body.first_password)
    return {"result": added_new_user} 






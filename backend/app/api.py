from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.model_serving_db import user_table
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
import jwt


class LoginBody(BaseModel):
    username: str
    password: str


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
       

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
    if login_status:
        token = jwt.encode({"public_id": body.username}, app.config["SECRET_KEY"], "HS256")
        return jsonify({"token":token})

    print(body)    
    return make_response("could not verify", 401, {"Authentication", "login required"})
#    return {"output": login_status}


@app.get("/search")
async def search():
    return {"data": "This should show a page with a search bar"}



@app.get("/create")
async def get_create():
    return {"data" : "A page for a new user to be born"}



@app.post("/create")
async def post_create():
    return {"data": "new user is created"}











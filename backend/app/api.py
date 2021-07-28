from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.model_serving_db import user_table

app = FastAPI()

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
async def login(user:dict):
    #add logic for checking user input
    print(user)
    login_status = user_table.check_valid_login("jisoo", "some password")
    
    return {"output": login_status}


@app.get("/search")
async def search():
    return {"data": "This should show a page with a search bar"}






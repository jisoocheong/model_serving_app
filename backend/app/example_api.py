from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from app.config import Settings, get_settings
from app.security import create_access_token
from app.auth import sign_up_new_user, authenticate_user, get_current_active_user
from app.model_serving_db.schemas import Token, User, Model
from app.model_serving_db.model_table import add_model, search_model


app = FastAPI()

# origins = [
#     "http://localhost:3000",
#     "localhost:3000"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    settings: Settings = Depends(get_settings)):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minute)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.post("/create_user")
async def create_user(new_user: User = Depends(sign_up_new_user)):
    return new_user


@app.post("/create_model")
async def create_model(new_model: Model = Depends(add_model)):
    return new_model


@app.get("/testing_img")
async def get_img():
    from fastapi.responses import FileResponse    
    return FileResponse("model_serving_db/img/pikachu.png" )
    
 
@app.get("/search")
async def get_searched_models(search: str):
    """
    This will get the id, name, version, framework, and tags of the models 
    """
    found_models = search_model(search)
    print(found_models)
    return {"found models" : found_models}


@app.get("/get_model")
async def get_model():
    """
    This will get the actual model with all the information that comes with it 
    """
    pass





@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return settings



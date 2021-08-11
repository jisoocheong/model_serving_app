from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
import security 
from config import Settings, get_settings
from security import create_access_token
from auth import sign_up_new_user, authenticate_user, get_current_active_user
from model_serving_db.schemas import Token, User, Model
from model_serving_db.model_table import edit_model, remove_model, add_model, search_model, get_model, show_img_by_id, get_first_img
from typing import List
from model_serving_db.user_table import all_user_info 


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

@app.post("/create_user")
async def create_user(settings: Settings = Depends(get_settings), new_user: User = Depends(sign_up_new_user)):
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username already taken",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minute)
    access_token = create_access_token(
        data={"sub": new_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/create_model")
async def create_model(new_model: Model = Depends(add_model)):
#    user = get_current_active_user(token)
    return new_model

@app.get("/search")
async def get_searched_models(model_name: str, token: str = Depends(security.oauth2_scheme)):
    """
    This will get the id, name, version, framework, tags, and description of the models 
    """
    found_models = search_model(model_name)
    return {"found models" : found_models}


@app.get("/get_model")
async def get_model(model: Model = Depends(get_model), token: str = Depends(security.oauth2_scheme)):
    """
    This will get the actual model with all the information that comes with it 
    """

    #model = get_model(name, version)
    if model is None:
        return "No model found"

    return model


@app.get("/get_img")
async def get_model_screenshot(id: int, token: str = Depends(security.oauth2_scheme)):
    from fastapi.responses import FileResponse    
    import base64
    img_path = get_first_img(id)
    return FileResponse(img_path) 



@app.post("/remove_model")
async def remove_model(model: Model = Depends(remove_model), token: str = Depends(security.oauth2_scheme)):
    return "Model removed"


@app.post("/edit_model") 
async def edit_model(model: Model = Depends(edit_model), token: str = Depends(security.oauth2_scheme)):
    return model


@app.get("/list_users")
async def get_all_users(token: str = Depends(security.oauth2_scheme)):
    return all_user_info()


@app.get("/list_models")
async def get_all_models(token: str = Depends(security.oauth2_scheme)):
    return search_model("")






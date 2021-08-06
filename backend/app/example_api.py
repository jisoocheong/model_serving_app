from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
import security 

from config import Settings, get_settings
from security import create_access_token
from auth import sign_up_new_user, authenticate_user, get_current_active_user
from model_serving_db.schemas import Token, User, Model
from model_serving_db.model_table import add_model, search_model, get_model_by_id, show_img_by_id, get_first_img



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
    return new_model

@app.get("/testing_img")
async def get_img():
    from fastapi.responses import FileResponse    
    return FileResponse("model_serving_db/img/cat.jpeg")

@app.get("/search")
async def get_searched_models(search: str, token: str = Depends(security.oauth2_scheme)):
    """
    This will get the id, name, version, framework, and tags of the models 
    """
    found_models = search_model(search)
    return {"found models" : found_models}


@app.get("/get_model")
async def get_model(id: int, token: str = Depends(security.oauth2_scheme)):
    """
    This will get the actual model with all the information that comes with it 
    """
    from fastapi.responses import FileResponse    
    model = get_model_by_id(id)
    if model is None:
        return "No model found"

    return model


@app.get("/get_img")
async def get_model_screenshot(id: int, token: str = Depends(security.oauth2_scheme)):
    from fastapi.responses import FileResponse    
    import base64
    img_path = get_first_img(id)
    return FileResponse(img_path) 


@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return settings






from typing import Union
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.routers import OrmarCRUDRouterUpdated

from app.auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database.database import database, metadata, engine
from app.database.schemas import Token, UserCreateUpdateSchema
from app.database.models import User


# Create a FastAPI object
app = FastAPI(
    # Set custom title for our app
    title="APISample (FastAPI)"
)

# Pur our database in the state of app
app.state.database = database
# Create all tables in database
metadata.create_all(engine)

# Create variable with authentication dependency
# to allow unauthorized users execute POST (Create) request
# to create a new user
AUTH_CRUD_DEPENDENCIES = [Depends(get_current_user)]

# Create our CRUD router
crud_router = OrmarCRUDRouterUpdated(
    schema=User,
    prefix='users',
    create_schema=UserCreateUpdateSchema,
    update_schema=UserCreateUpdateSchema,
    update_route=AUTH_CRUD_DEPENDENCIES,
    delete_all_route=AUTH_CRUD_DEPENDENCIES,
    delete_one_route=AUTH_CRUD_DEPENDENCIES,
    get_all_route=AUTH_CRUD_DEPENDENCIES,
    get_one_route=AUTH_CRUD_DEPENDENCIES
)


# Include our CRUD router to app
app.include_router(crud_router)


@app.post("/token", response_model=Token, description="Get JWT token from a pair of username and password")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Union[HTTPException, dict]:
    """
    Login user and return access token.
    :param form_data:
    :return:
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.on_event('startup')
async def connect_to_database() -> None:
    """
    Connect to database with app startup
    :return:
    """
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event('shutdown')
async def disconnect_from_database() -> None:
    """
    Disconnect from database with app shutdown
    :return:
    """
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()

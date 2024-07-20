from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.user.auth import authenticate_user, create_access_token, get_password_hash, verify_password
from app.user.dao import UserDAO
from app.user.dependencies import get_current_user
from app.user.models import User
from app.user.schemas import SchemaUserLogin, SchemaUserRegister
from uuid import UUID


router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"],
)


@router.post("/register")
async def register_user(user_data: SchemaUserRegister):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SchemaUserLogin):
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("menu_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("menu_access_token")


@router.get("/me")
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{id}", response_model=SchemaUserLogin)  
async def get_single_user(id: UUID):
    single_user = await UserDAO.find_by_id(id)
    if not single_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user not found"
                            )
    return single_user
from fastapi import APIRouter, HTTPException
from controllers.user_controller import *
from models.user_models import Users

router = APIRouter()

nuevo_usuario = UsersController()


@router.post("/create_users")
async def create_user(user: Users):
    rpta = nuevo_usuario.create_user(user)
    return rpta


@router.get("/get_user/{user_id}",response_model=Users)
async def get_user(user_id: int):
    rpta = nuevo_usuario.get_user(user_id)
    return rpta

@router.get("/get_users/")
async def get_users():
    rpta = nuevo_usuario.get_users()
    return rpta

@router.put("/edit_user/{id}")
async def edit_user(id:int, user:Users):
    rpta = nuevo_usuario.edit_user(id,user)
    return rpta

@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    rpta = nuevo_usuario.delete_user(user_id)
    return rpta

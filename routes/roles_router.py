from fastapi import APIRouter, HTTPException
from controllers.roles_controller import RolesController
from models.roles_models import roles

router = APIRouter()
roles_controller = RolesController()

@router.post("/create_role")
async def create_role(role: roles):
    rpta = roles_controller.create_role(role)
    return rpta

@router.get("/get_role/{role_id}")
async def get_role(role_id: int):
    rpta = roles_controller.get_role(role_id)
    return rpta

@router.get("/get_roles")
async def get_roles():
    rpta = roles_controller.get_roles()
    return rpta

@router.put("/edit_role/{role_id}")
async def edit_role(role_id: int, role: roles):
    rpta = roles_controller.edit_role(role_id, role)
    return rpta

@router.delete("/delete_role/{role_id}")
async def delete_role(role_id: int):
    rpta = roles_controller.delete_role(role_id)
    return rpta
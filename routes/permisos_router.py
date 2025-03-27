from fastapi import APIRouter
from controllers.permisos_controller import PermisosController
from models.permisos_models import permisos
from typing import List, Optional

router = APIRouter()
permisos_controller = PermisosController()

@router.post("/create_permiso")
async def create_permiso(permiso: permisos):
    rpta = permisos_controller.create_permiso(permiso)
    return rpta

@router.get("/get_permiso/{permiso_id}")
async def get_permiso(permiso_id: int):
    rpta = permisos_controller.get_permiso(permiso_id)
    return rpta

@router.get("/get_permisos")
async def get_permisos():
    rpta = permisos_controller.get_permisos()
    return rpta

@router.put("/edit_permiso/{permiso_id}")
async def edit_permiso(permiso_id: int, permiso: permisos):
    rpta = permisos_controller.edit_permiso(permiso_id, permiso)
    return rpta

@router.delete("/delete_permiso/{permiso_id}")
async def delete_permiso(permiso_id: int):
    rpta = permisos_controller.delete_permiso(permiso_id)
    return rpta


@router.get("/get_permisos_por_rol/{rol_id}")
async def get_permisos_por_rol(rol_id: int):
    rpta = permisos_controller.get_permisos_por_rol(rol_id)
    return rpta

@router.put("/edit_permisos_por_rol/{rol_id}")
async def edit_permisos_por_rol(rol_id: int, permisos: List[permisos]):
    rpta = permisos_controller.edit_permisos_por_rol(rol_id, permisos)
    return rpta
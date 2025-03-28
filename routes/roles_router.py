from fastapi import APIRouter, HTTPException
from controllers.roles_controller import RolesController
from models.roles_models import Roles
from typing import Optional

router = APIRouter(
    prefix="/roles",
    tags=["Gestión de Roles"],
    responses={
        404: {"description": "Rol no encontrado"},
        400: {"description": "Solicitud inválida"},
        500: {"description": "Error interno del servidor"}
    }
)

controller = RolesController()

@router.post("/crear", response_model=dict, status_code=201)
async def crear_rol(rol: Roles):
    """
    Crea un nuevo rol en el sistema.
    
    Campos requeridos:
    - nombre (string, máximo 50 caracteres)
    - estado (boolean)
    """
    return controller.crear_rol(rol)

@router.get("/listar", response_model=dict)
async def listar_roles():
    """Lista todos los roles activos ordenados alfabéticamente"""
    return controller.listar_roles()

@router.get("/obtener/{rol_id}", response_model=dict)
async def obtener_rol(rol_id: int):
    """Obtiene un rol específico por su ID"""
    return controller.obtener_rol(rol_id)

@router.put("/actualizar/{rol_id}", response_model=dict)
async def actualizar_rol(rol_id: int, rol: Roles):
    """Actualiza los datos de un rol existente"""
    return controller.actualizar_rol(rol_id, rol)

@router.delete("/eliminar/{rol_id}", response_model=dict)
async def eliminar_rol(rol_id: int):
    """Elimina lógicamente un rol (soft delete)"""
    return controller.eliminar_rol(rol_id)
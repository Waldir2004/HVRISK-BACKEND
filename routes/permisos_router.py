from fastapi import APIRouter, HTTPException
from controllers.permisos_controller import PermisosController
from models.permisos_models import Permisos
from typing import List

router = APIRouter(
    prefix="/permisos",
    tags=["Gestión de Permisos"],
    responses={
        404: {"description": "Recurso no encontrado"},
        400: {"description": "Solicitud inválida"},
        500: {"description": "Error interno del servidor"}
    }
)

controller = PermisosController()

@router.post("/crear", response_model=dict, status_code=201)
async def crear_permiso(permiso: Permisos):
    """
    Asigna un nuevo permiso a un rol.
    
    Campos requeridos:
    - modulo_id (int): ID del módulo
    - rol_id (int): ID del rol
    - estado (bool): Estado del permiso
    """
    return controller.crear_permiso(permiso)

@router.get("/listar", response_model=dict)
async def listar_permisos():
    """Lista todos los permisos con información de módulos y roles"""
    return controller.listar_permisos()

@router.get("/obtener/{permiso_id}", response_model=dict)
async def obtener_permiso(permiso_id: int):
    """Obtiene un permiso específico con información relacionada"""
    return controller.obtener_permiso(permiso_id)

@router.put("/actualizar/{permiso_id}", response_model=dict)
async def actualizar_permiso(permiso_id: int, permiso: Permisos):
    """Actualiza un permiso existente"""
    return controller.actualizar_permiso(permiso_id, permiso)

@router.delete("/eliminar/{permiso_id}", response_model=dict)
async def eliminar_permiso(permiso_id: int):
    """Elimina lógicamente un permiso"""
    return controller.eliminar_permiso(permiso_id)

@router.get("/por-rol/{rol_id}", response_model=dict)
async def listar_permisos_por_rol(rol_id: int):
    """Lista todos los módulos permitidos para un rol específico"""
    return controller.listar_permisos_por_rol(rol_id)

@router.put("/actualizar-por-rol/{rol_id}", response_model=dict)
async def actualizar_permisos_rol(rol_id: int, permisos: List[Permisos]):
    """
    Actualiza masivamente los permisos de un rol.
    Reemplaza todos los permisos existentes por los nuevos.
    """
    return controller.actualizar_permisos_rol(rol_id, permisos)
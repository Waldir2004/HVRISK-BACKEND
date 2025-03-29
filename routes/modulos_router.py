from fastapi import APIRouter, HTTPException
from controllers.modulos_controller import ModulosController
from models.modulos_models import Modulos
from typing import Optional

router = APIRouter(
    prefix="/modulos",
    tags=["Módulos del Sistema"],
    responses={404: {"description": "Módulo no encontrado"}}
)

controller = ModulosController()

@router.post("/crear", response_model=dict, status_code=201)
async def crear_modulo(modulo: Modulos):
    """Registra un nuevo módulo en el sistema"""
    return controller.crear_modulo(modulo)

@router.get("/listar", response_model=dict)
async def listar_modulos():
    """Obtiene todos los módulos activos"""
    return controller.listar_modulos()

@router.get("/obtener/{modulo_id}", response_model=dict)
async def obtener_modulo(modulo_id: int):
    """Obtiene un módulo específico por su ID"""
    return controller.obtener_modulo(modulo_id)

@router.put("/actualizar/{modulo_id}", response_model=dict)
async def actualizar_modulo(modulo_id: int, modulo: Modulos):
    """Actualiza los datos de un módulo existente"""
    return controller.actualizar_modulo(modulo_id, modulo)

@router.delete("/eliminar/{modulo_id}", response_model=dict)
async def eliminar_modulo(modulo_id: int):
    """Elimina lógicamente un módulo (soft delete)"""
    return controller.eliminar_modulo(modulo_id)
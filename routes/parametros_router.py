from fastapi import APIRouter, HTTPException
from controllers.parametros_controller import ParametrosController
from models.parametros_models import Parametros
from typing import Optional

router = APIRouter(
    prefix="/parametros",
    tags=["Parámetros del Sistema"],
    responses={
        404: {"description": "Parámetro no encontrado"},
        422: {"description": "Error de validación"},
        500: {"description": "Error interno del servidor"}
    }
)

controller = ParametrosController()

@router.post("/crear", response_model=dict, status_code=201)
async def crear_parametro(parametro: Parametros):
    """
    Crea un nuevo parámetro en el sistema.
    
    Campos requeridos:
    - referencia (string, máximo 20 caracteres)
    - nombre (string)
    - estado (boolean)
    """
    return controller.crear_parametro(parametro)

@router.get("/listar", response_model=dict)
async def listar_parametros():
    """Lista todos los parámetros activos ordenados por nombre"""
    return controller.listar_parametros()

@router.get("/obtener/{parametro_id}", response_model=dict)
async def obtener_parametro(parametro_id: int):
    """Obtiene un parámetro específico por su ID"""
    return controller.obtener_parametro(parametro_id)

@router.put("/actualizar/{parametro_id}", response_model=dict)
async def actualizar_parametro(parametro_id: int, parametro: Parametros):
    """Actualiza los datos de un parámetro existente"""
    return controller.actualizar_parametro(parametro_id, parametro)

@router.delete("/eliminar/{parametro_id}", response_model=dict)
async def eliminar_parametro(parametro_id: int):
    """Elimina lógicamente un parámetro (soft delete)"""
    return controller.eliminar_parametro(parametro_id)
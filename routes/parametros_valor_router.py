from fastapi import APIRouter, HTTPException
from controllers.parametros_valor_controller import ParametrosValorController
from models.parametros_valor_models import ParametrosValor
from typing import Optional

router = APIRouter(
    prefix="/parametros-valor",
    tags=["Valores de Parámetros"],
    responses={
        404: {"description": "Recurso no encontrado"},
        400: {"description": "Solicitud inválida"},
        500: {"description": "Error interno del servidor"}
    }
)

controller = ParametrosValorController()

@router.post("/crear", response_model=dict, status_code=201)
async def crear_parametro_valor(parametro_valor: ParametrosValor):
    """
    Crea un nuevo valor para un parámetro existente.
    
    Campos requeridos:
    - referencia (string, max 20 chars)
    - nombre (string)
    - parametro_id (int, ID de parámetro existente)
    - estado (boolean)
    """
    return controller.crear_parametro_valor(parametro_valor)

@router.get("/listar", response_model=dict)
async def listar_parametros_valores():
    """Lista todos los valores de parámetros con información del parámetro padre"""
    return controller.listar_parametros_valores()

@router.get("/obtener/{parametro_valor_id}", response_model=dict)
async def obtener_parametro_valor(parametro_valor_id: int):
    """Obtiene un valor específico con información del parámetro asociado"""
    return controller.obtener_parametro_valor(parametro_valor_id)

@router.put("/actualizar/{parametro_valor_id}", response_model=dict)
async def actualizar_parametro_valor(parametro_valor_id: int, parametro_valor: ParametrosValor):
    """Actualiza un valor de parámetro existente"""
    return controller.actualizar_parametro_valor(parametro_valor_id, parametro_valor)

@router.delete("/eliminar/{parametro_valor_id}", response_model=dict)
async def eliminar_parametro_valor(parametro_valor_id: int):
    """Elimina lógicamente un valor de parámetro"""
    return controller.eliminar_parametro_valor(parametro_valor_id)

@router.get("/por-parametro/{parametro_id}", response_model=dict)
async def listar_valores_por_parametro(parametro_id: int):
    """Obtiene todos los valores asociados a un parámetro específico"""
    return controller.listar_valores_por_parametro(parametro_id)
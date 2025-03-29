from fastapi import APIRouter, HTTPException
from controllers.evaluaciones_controller import EvaluacionesController
from models.evaluaciones_model import Evaluaciones
from typing import Optional

router = APIRouter(
    prefix="/evaluaciones",
    tags=["Evaluación de Riesgo Cardiovascular"],
    responses={
        404: {"description": "Evaluación no encontrada"},
        500: {"description": "Error interno del servidor"}
    }
)

controller = EvaluacionesController()

@router.post("/crear", response_model=dict, status_code=201)
async def crear_evaluacion(evaluacion: Evaluaciones):
    """Crea una nueva evaluación de riesgo cardiovascular"""
    return controller.create_evaluacion(evaluacion)

@router.get("/listar", response_model=dict)
async def listar_evaluaciones(paciente_id: Optional[int] = None):
    """Lista evaluaciones, con filtro opcional por paciente"""
    return controller.get_evaluaciones(paciente_id)

@router.get("/obtener/{evaluacion_id}", response_model=dict)
async def obtener_evaluacion(evaluacion_id: int):
    """Obtiene una evaluación específica por su ID"""
    return controller.get_evaluacion_by_id(evaluacion_id)

@router.put("/actualizar/{evaluacion_id}", response_model=dict)
async def actualizar_evaluacion(evaluacion_id: int, evaluacion: Evaluaciones):
    """Actualiza una evaluación existente"""
    return controller.update_evaluacion(evaluacion_id, evaluacion)

@router.delete("/eliminar/{evaluacion_id}", response_model=dict)
async def eliminar_evaluacion(evaluacion_id: int):
    """Elimina lógicamente una evaluación"""
    return controller.delete_evaluacion(evaluacion_id)
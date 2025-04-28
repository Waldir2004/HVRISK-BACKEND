# evaluaciones_completas_router.py
from fastapi import APIRouter, Depends, HTTPException
from controllers.evaluaciones_completas_controller import EvaluacionesCompletasController
from typing import Dict, Any

router = APIRouter(
    prefix="/evaluaciones-completas",
    tags=["Evaluaciones Completas"],
    responses={404: {"description": "No encontrado"}}
)

@router.post("/crear", response_model=dict, status_code=201)
async def crear_evaluacion_completa(
    datos: Dict[str, Any],
    controller: EvaluacionesCompletasController = Depends()
):
    """Crea una evaluación completa con todos sus registros asociados"""
    try:
        return controller.crear_evaluacion_completa(datos)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
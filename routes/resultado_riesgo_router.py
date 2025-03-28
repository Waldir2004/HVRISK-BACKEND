from fastapi import APIRouter, HTTPException
from controllers.resultado_riesgo_controller import ResultadoRiesgoController
from models.resultado_riesgo_model import ResultadosRiesgo
from typing import Optional

router = APIRouter(
    prefix="/resultados-riesgo",
    tags=["Evaluación de Riesgo Cardiovascular"],
    responses={
        404: {"description": "Evaluación no encontrada"},
        500: {"description": "Error interno del servidor"}
    }
)

controller = ResultadoRiesgoController()

@router.post("/crear", response_model=dict, status_code=201)
async def crear_resultado(resultado: ResultadosRiesgo):
    return controller.crear_resultado(resultado)

@router.get("/listar", response_model=dict)
async def listar_resultados(paciente_id: Optional[int] = None):
    return controller.listar_resultados(paciente_id)

@router.get("/obtener/{resultado_id}", response_model=dict)
async def obtener_resultado(resultado_id: int):
    return controller.obtener_resultado(resultado_id)

@router.put("/actualizar/{resultado_id}", response_model=dict)
async def actualizar_resultado(resultado_id: int, resultado: ResultadosRiesgo):
    return controller.actualizar_resultado(resultado_id, resultado)

@router.delete("/eliminar/{resultado_id}", response_model=dict)
async def eliminar_resultado(resultado_id: int):
    return controller.eliminar_resultado(resultado_id)
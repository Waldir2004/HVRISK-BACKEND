from fastapi import APIRouter, HTTPException
from controllers.estilo_vida_controller import EstiloVidaController
from models.estilo_vida_model import EstiloVida
from typing import Optional

router = APIRouter(
    prefix="/estilo-vida",
    tags=["Estilo de Vida"],
    responses={
        404: {"description": "Registro no encontrado"},
        500: {"description": "Error interno del servidor"}
    }
)

controller = EstiloVidaController()

@router.post("/crear", response_model=dict, status_code=201)
async def crear_estilo(estilo: EstiloVida):
    """Crea un nuevo registro de estilo de vida"""
    return controller.create_estilo_vida(estilo)

@router.get("/listar", response_model=dict)
async def listar_estilos(evaluacion_id: Optional[int] = None):
    """Lista registros de estilo de vida, con filtro opcional por evaluación"""
    return controller.get_estilos_vida(evaluacion_id)

@router.get("/obtener/{estilo_id}", response_model=dict)
async def obtener_estilo(estilo_id: int):
    """Obtiene un registro específico por su ID"""
    return controller.get_estilo_vida_by_id(estilo_id)

@router.put("/actualizar/{estilo_id}", response_model=dict)
async def actualizar_estilo(estilo_id: int, estilo: EstiloVida):
    """Actualiza un registro existente de estilo de vida"""
    return controller.update_estilo_vida(estilo_id, estilo)

@router.delete("/eliminar/{estilo_id}", response_model=dict)
async def eliminar_estilo(estilo_id: int):
    """Elimina lógicamente un registro de estilo de vida"""
    return controller.delete_estilo_vida(estilo_id)
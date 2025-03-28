from fastapi import APIRouter, HTTPException
from controllers.estilo_vida_controller import EstiloVidaController
from models.estilo_vida_model import EstiloVida
from typing import Optional

router = APIRouter(
    prefix="/estilo-vida",
    tags=["Estilo de Vida"],
    responses={404: {"description": "No encontrado"}}
)

controller = EstiloVidaController()

@router.post("/crear", response_model=dict, status_code=201)
async def crear_estilo(estilo: EstiloVida):
    return controller.crear_estilo_vida(estilo)

@router.get("/listar", response_model=dict)
async def listar_estilos(paciente_id: Optional[int] = None):
    return controller.listar_estilos_vida(paciente_id)

@router.get("/obtener/{estilo_id}", response_model=dict)
async def obtener_estilo(estilo_id: int):
    return controller.obtener_estilo_vida(estilo_id)

@router.put("/actualizar/{estilo_id}", response_model=dict)
async def actualizar_estilo(estilo_id: int, estilo: EstiloVida):
    return controller.actualizar_estilo_vida(estilo_id, estilo)

@router.delete("/eliminar/{estilo_id}", response_model=dict)
async def eliminar_estilo(estilo_id: int):
    return controller.eliminar_estilo_vida(estilo_id)